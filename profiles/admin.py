"Profile Admin Models"

from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile, Subscription


class ProfileInline(admin.StackedInline):
    """
    Inline representation of user profiles for the admin panel.

    """

    model = UserProfile
    extra = 0


class UserAdmin(admin.ModelAdmin):
    """
    Admin model configuration for user accounts.

    This class defines the admin panel configuration for user accounts,
    allowing administrators to manage user information such as username,
    first name, last name, and email. It also includes an inline
    representation of user profiles using the `ProfileInline` class

    Example:
        To use this admin configuration for user accounts:

        admin.site.register(User, UserAdmin)

    """

    model = User
    fields = ("username", "first_name", "last_name", "email", 'is_superuser')
    inlines = [ProfileInline]


class SubscriptionAdmin(admin.ModelAdmin):
    """
    Admin interface customization for managing Subscription model.

    """
    model = Subscription


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
