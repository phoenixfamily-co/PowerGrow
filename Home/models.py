
from django.db import models
from django.utils import timezone


# Create your models here.

class Slider(models.Model):
    image = models.ImageField(upload_to="images/")
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    datetime = models.DateTimeField(default=timezone.now)
