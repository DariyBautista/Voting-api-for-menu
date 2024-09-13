from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

class CustomUserManager(BaseUserManager):
    """
    Manager for creating users and superusers.

    Methods:
        create_user(email, password, **extra_fields): Creates and returns a regular user with the given email and password.
        create_superuser(email, password, **extra_fields): Creates and returns a superuser with the given email and password.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Creates and returns a regular user with the given email and password.

        Args:
            email (str): The email address for the user.
            password (str): The password for the user.
            **extra_fields: Additional fields for the user.

        Returns:
            CustomUser: The created user.
        
        Raises:
            ValueError: If the email is not provided.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and returns a superuser with the given email and password.

        Args:
            email (str): The email address for the superuser.
            password (str): The password for the superuser.
            **extra_fields: Additional fields for the superuser.

        Returns:
            CustomUser: The created superuser.

        Raises:
            ValueError: If `is_staff` or `is_superuser` is not set to True.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for authentication.

    Attributes:
        id (int): The unique identifier for the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user.
        phone_number (str): The phone number of the user.
        is_active (bool): Whether the user account is active.
        is_staff (bool): Whether the user has staff status.
        is_superuser (bool): Whether the user has superuser status.

    Methods:
        __str__(): Returns the email address of the user.
    """

    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']
    objects = CustomUserManager()

    def __str__(self):
        """
        Returns the email address of the user.

        Returns:
            str: The email address of the user.
        """
        return self.email
