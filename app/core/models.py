"""Database models."""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, #contains the functionality for the auth system
    BaseUserManager,
    PermissionsMixin, #contains the functionality for the permissions and fields
)

"""user model manager """
class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields): #creating a user without a password for testing
        """Create , save and return a new user"""
        if not email:
            raise ValueError('User must have an email address.')

        user = self.model(email=self.normalize_email(email), **extra_fields) #keyword arguments if we define other fields without updating the method
        #self.model is the same as accessing User class
        user.set_password(password)
        user.save(using=self._db) #best practice to save the user to the working db, in case we work with another db

        return user

    def create_superuser(self, email, password,**extra_fields):
        """Create and return a new superuser."""
        if password is None:
         raise ValueError('Superuser must have a password.')

        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager() #assigning the user to custom user manager --> important

    USERNAME_FIELD = 'email' #defines the field used for authentication