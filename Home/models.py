
from django.db import models
from django.utils import timezone


# Create your models here.

class Slider(models.Model):
    image = models.ImageField(upload_to="images/", blank=True, null=True, verbose_name="عکس")
    title = models.TextField(blank=True, null=True, verbose_name="نام")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    datetime = models.DateTimeField(default=timezone.now)
