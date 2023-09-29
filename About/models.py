from django.db import models
from django.utils import timezone


class AboutUs(models.Model):
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    telegram = models.CharField(max_length=50, null=True, blank=True)
    instagram = models.CharField(max_length=50, null=True, blank=True)
    telephone = models.CharField(max_length=11, null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    logo = models.ImageField(upload_to="images/", blank=True, null=True)
    transparent_logo = models.ImageField(upload_to="images/", blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    latitude = models.FloatField(default=0 , blank=True, null=True)
    longitude = models.FloatField(default=0 , blank=True, null=True)
    datetime = models.DateTimeField(default=timezone.now)
