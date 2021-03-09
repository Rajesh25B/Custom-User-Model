from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, \
                                        BaseUserManager
 

class UserManager(BaseUserManager):
    """
    Extend the BaseUserManager and pull the basic features from it
    and overwrite a couple of functions to handle our email instead
    of username
    """

    def create_user(self, email, password=None, **extra_fields):
        """Create and saves a new `User`."""

        if not email:
            raise ValueError('Enter Value email address')

        user = self.model(email = self.normalize_email(email), **extra_fields)

        if password:
            user.set_password(password)
        
        user.save()

        return user
    
    def create_superuser(self, email, password):
        """creating a superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(max_length=15, db_index=True)
    email = models.EmailField(max_length=75, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()
    USERNAME_FIELD = 'email'
    # Email & Password are required by default.
    REQUIRED_FIELDS = []

    # String representation
    def __str__(self):
        return self.name
