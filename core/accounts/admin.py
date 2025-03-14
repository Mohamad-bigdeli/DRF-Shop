from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ShopUser, Profile
from .forms import ShopUserCreationForm, ShopUserChangeForm


class CustomUserAdmin(UserAdmin):
    """
    Custom admin panel for user management with add and change forms plus password
    """

    model = ShopUser
    form = ShopUserChangeForm
    add_form = ShopUserCreationForm
    list_display = ("phone", "email", "google_id", "is_superuser", "is_active", "is_verified")
    list_filter = ("phone", "email", "google_id", "is_superuser", "is_active", "is_verified")
    searching_fields = ("phone",)
    ordering = ("phone",)
    filter_horizontal = []
    fieldsets = (
        (
            "Authentication",
            {
                "fields": ("phone", "password"),
            },
        ),
        (
            "permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                ),
            },
        ),
        (
            "group permissions",
            {
                "fields": ("groups", "user_permissions"),
            },
        ),
        (
            "important date",
            {
                "fields": ("last_login",),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone",
                    "email",
                    "google_id",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                ),
            },
        ),
    )

admin.site.register(ShopUser, CustomUserAdmin)
admin.site.register(Profile)