from django.db import models
from django.utils import timezone


class AboutUs(models.Model):
    title = models.TextField(blank=True, null=True, verbose_name="نام")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    telegram = models.CharField(max_length=50, null=True, blank=True, verbose_name="تلگرام")
    instagram = models.CharField(max_length=50, null=True, blank=True, verbose_name="اینستاگرام")
    telephone = models.CharField(max_length=11, null=True, blank=True, verbose_name="تلفن")
    phone = models.CharField(max_length=13, null=True, blank=True, verbose_name="موبایل")
    logo = models.ImageField(upload_to="images/", blank=True, null=True, verbose_name="لوگو")
    transparent_logo = models.ImageField(upload_to="images/", blank=True, null=True, verbose_name="لوگو بدون پس زمینه")
    address = models.TextField(null=True, blank=True, verbose_name="آدرس")
    latitude = models.FloatField(default=0, blank=True, null=True, verbose_name="عرض جغرافیایی")
    longitude = models.FloatField(default=0, blank=True, null=True, verbose_name="طول جغرافیایی")
    datetime = models.DateTimeField(default=timezone.now)
