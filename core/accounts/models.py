from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from .managers import ShopUserManager

# Create your models here.

class ShopUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model for our app
    """

    phone = models.CharField(max_length=11, unique=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    google_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = ShopUserManager()

    def __str__(self):
        return self.phone

class Profile(models.Model):
    """
    A model for user information's
    """
    user = models.OneToOneField(ShopUser, on_delete=models.CASCADE, related_name="user")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    image = models.ImageField(upload_to="profile-pictures/", blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.phone