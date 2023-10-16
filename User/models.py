from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

SALARY_CHOICE = (
    ('آزاد', 'free'),
    ('درصدی', 'percentage'),
    ('ثابت', 'static'),
)


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
    name = models.CharField(max_length=50)
    number = PhoneNumberField(unique=True)
    address = models.TextField(default="آدرس", blank=True, null=True)
    email = models.EmailField(default="ایمیل" , blank=True, null=True)
    telephone = models.IntegerField(default="تلفن ثابت", blank=True, null=True)
    accountNumber = models.TextField(default="شماره حساب",blank=True, null=True)
    accountId = models.TextField(default="شماره شبا",blank=True, null=True)
    zipCode = models.IntegerField(default="کدپستی",blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    birthdate = models.CharField(max_length=10, default=timezone.now)
    national = models.IntegerField(blank=True, null=True, unique=True)
    gender = models.CharField(max_length=10)
    salary = models.CharField(max_length=20, choices=SALARY_CHOICE)
    fee = models.IntegerField(null=True, blank=True)
    created = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    datetime = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'number'
    REQUIRED_FIELDS = ['name', 'password', 'gender', 'birthdate']

    objects = CustomAccountManager()

    def __str__(self):
        return str(self.number)
