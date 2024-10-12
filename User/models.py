from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

SALARY_CHOICE = (
    ('درصدی', 'درصدی'),
    ('ثابت', 'ثابت'),
)

DEBT_CHOICE = (
    ('بدهکار', 'بدهکار'),
    ('تسویه', 'تسویه'),
    ('پستانکار', 'پستانکار'),

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
    name = models.TextField(verbose_name="نام نام خانوادگی")
    number = PhoneNumberField(unique=True, verbose_name="شماره تلفن")
    email = models.EmailField(blank=True, null=True, verbose_name="ایمیل")
    is_staff = models.BooleanField(default=False, verbose_name="مدیر")
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_superuser = models.BooleanField(default=False, verbose_name='منشی')
    is_teacher = models.BooleanField(default=False, verbose_name='مربی')
    birthdate = models.TextField(default=timezone.now, verbose_name='تاریخ تولد')
    salary = models.CharField(max_length=20, choices=SALARY_CHOICE, blank=True, null=True, verbose_name="نوع حقوق")
    fee = models.IntegerField(null=True, blank=True, verbose_name="مقدار حقوق")
    situation = models.CharField(max_length=20, choices=DEBT_CHOICE, blank=True, null=True, verbose_name="وضعیت بدهی")
    debt = models.IntegerField(null=True, blank=True, verbose_name="مقدار بدهی")
    description = models.TextField(null=True, blank=True, verbose_name="توضیحات")
    created = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    datetime = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'number'
    REQUIRED_FIELDS = ['name', 'password', 'birthdate']

    objects = CustomAccountManager()

    def __str__(self):
        return str(self.number)
