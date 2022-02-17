# django builtin imports
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.conf import settings

# Custome imports
from .managers.user_manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports email"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tag to be used for recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.name
