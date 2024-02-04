"""Database models."""
import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, #contains the functionality for the auth system
    BaseUserManager,
    PermissionsMixin, #contains the functionality for the permissions and fields
)

def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}' #whatever extension jpg or png etc

    return os.path.join('uploads', 'recipe', filename) #generate a path for the uploaded image

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


class Recipe(models.Model):
    """Recipe object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )  #recipes belong to a user
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title

class Tag(models.Model):
    """Tag for filtering recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient for recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name