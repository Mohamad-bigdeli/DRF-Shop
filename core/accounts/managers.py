from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class ShopUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, phone, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password and extra data.
        """
        if not phone:
            raise ValueError(_("The Phone field must be set"))
        if email:
            email = self.normalize_email(email)
        user = self.model(phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password and extra data.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is is_superuser=True"))

        return self.create_user(phone, email, password, **extra_fields)
