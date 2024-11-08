from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from django.utils import timezone


class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    upvoted_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='upvoted_tips', blank=True)
    downvoted_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='downvoted_tips', blank=True)

    def upvotes_count(self):
        """Returns the number of upvotes for this tip."""
        return self.upvoted_by.count()

    def downvotes_count(self):
        """Returns the number of downvotes for this tip."""
        return self.downvoted_by.count()

    @staticmethod
    def can_user_downvote(user):
        """Checks if a user has at least two upvotes across their own tips and has permission to downvote."""
        if not user.can_downvote:
            return False  # Immediately return False if the user is not allowed to downvote

        user_tips = Tip.objects.filter(author=user)
        total_upvotes = sum(tip.upvotes_count() for tip in user_tips)
        return total_upvotes >= 2  # Check if the user has at least two upvotes


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
    can_downvote = models.BooleanField(default=True)  # New field to enable/disable downvote ability

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
