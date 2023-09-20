from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, number, password, **other_fields):
        other_fields.setdefault('is_staff', False)
        other_fields.setdefault('is_superuser', False)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_admin', False)

        return self.create_user(number, password, **other_fields)

    def create_user(self, number, password, **other_fields):
        user = self.model(number=number, **other_fields)
        user.set_password(password)
        user.save()
        return User


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50, default="unknown")
    number = PhoneNumberField(unique=True, )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    password = models.CharField(max_length=32)
    birthdate = models.CharField(max_length=10, default=timezone.now)
    national = PhoneNumberField(unique=True, blank=True, null=True)
    gender = models.CharField(max_length=10)
    USERNAME_FIELD = 'number'
    REQUIRED_FIELDS = ['name', 'password', 'gender', 'birthdate']

    objects = CustomAccountManager()
