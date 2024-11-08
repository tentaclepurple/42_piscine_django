from django.contrib import admin
from .models import Tip, CustomUser
from django.contrib.auth.admin import UserAdmin

# CustomUserAdmin configuration to match the fields available in CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Define custom fieldsets for CustomUser, excluding email, first_name, and last_name
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Custom Permissions', {'fields': ('can_downvote',)}),  # Custom field added for downvote control
    )
    # Customize the list_display and make date_joined readonly
    list_display = ('username', 'date_joined', 'is_active', 'is_staff', 'can_downvote')
    readonly_fields = ('date_joined',)  # Make date_joined read-only
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
