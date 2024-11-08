from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Tip

# Register CustomUser with a custom admin configuration
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Define the custom fieldsets, including reputation as read-only
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Reputation & Custom Permissions', {'fields': ('reputation', 'can_downvote', 'can_delete')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # Display username, reputation, and other fields in the user list
    list_display = ('username', 'reputation', 'is_active', 'is_staff', 'can_downvote', 'can_delete')
    readonly_fields = ('reputation', 'date_joined')  # Make reputation read-only in the admin panel
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username',)

# Register the Tip model with custom configuration
@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'date', 'upvotes_count', 'downvotes_count')  # Display fields in list view
    search_fields = ('content', 'author__username')  # Fields used for search
    readonly_fields = ('upvotes_count', 'downvotes_count')  # Read-only fields in admin form

    def upvotes_count(self, obj):
        """Display the number of upvotes."""
        return obj.upvoted_by.count()
    
    def downvotes_count(self, obj):
        """Display the number of downvotes."""
        return obj.downvoted_by.count()
