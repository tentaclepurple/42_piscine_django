from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The username field is required')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    reputation = models.IntegerField(default=0)  # Reputation starts at 0
    can_downvote = models.BooleanField(default=True)  # Manual downvote permission
    can_delete = models.BooleanField(default=False)   # Manual delete permission

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    def update_reputation(self):
        """Calculates and updates the user's reputation based on votes on their tips."""
        upvotes = sum(tip.upvoted_by.count() for tip in self.tips.all())
        downvotes = sum(tip.downvoted_by.count() for tip in self.tips.all())
        # Each upvote adds 5 points, each downvote subtracts 2 points
        self.reputation = (upvotes * 5) - (downvotes * 2)
        self.save()

    def can_downvote_permission(self):
        """Returns True if the user has either manual or reputation-based downvote permission."""
        return self.can_downvote or self.reputation >= 15

    def can_delete_permission(self):
        """Returns True if the user has either manual or reputation-based delete permission."""
        return self.can_delete or self.reputation >= 30

    def __str__(self):
        # Display username with reputation in parentheses
        return f"{self.username} ({self.reputation})"


class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tips', on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    upvoted_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='upvoted_tips', blank=True)
    downvoted_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='downvoted_tips', blank=True)

    def save(self, *args, **kwargs):
        """Override save to ensure author reputation updates on tip save."""
        super().save(*args, **kwargs)
        self.author.update_reputation()

    def delete(self, *args, **kwargs):
        """Override delete to remove tip's influence on author's reputation."""
        super().delete(*args, **kwargs)
        self.author.update_reputation()

    def upvote(self, user):
        """Adds an upvote from a user and recalculates author's reputation."""
        if user not in self.upvoted_by.all():
            self.upvoted_by.add(user)
            self.downvoted_by.remove(user)
            self.author.update_reputation()

    def downvote(self, user):
        """Adds a downvote from a user and recalculates author's reputation."""
        if user not in self.downvoted_by.all():
            self.downvoted_by.add(user)
            self.upvoted_by.remove(user)
            self.author.update_reputation()
