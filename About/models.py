from django.db import models


class AboutUs(models.Model):
    telegram = models.CharField(max_length=50, null=True, unique=True)
    instagram = models.CharField(max_length=50, null=True, unique=True)
    telephone = models.CharField(max_length=11, null=True, unique=True)
    phone = models.CharField(max_length=13, null=True, unique=True)
    logo = models.ImageField(upload_to="images/", blank=True, null=True)
    transparent_logo = models.ImageField(upload_to="images/", blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
