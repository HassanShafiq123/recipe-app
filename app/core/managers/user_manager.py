from django.contrib.auth.models import (
    BaseUserManager
    )


class UserManager(BaseUserManager):
    """Custom user manager to impelement Custom User model"""

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a new User"""
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """
        Create and save a new super user
        Args:
            email ([type]): [description]
            password ([type]): [description]
        """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
