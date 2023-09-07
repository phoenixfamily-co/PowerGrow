
from django.db import models
from django.utils import timezone


# Create your models here.

class Slider(models.Model):
    image = models.ImageField(upload_to="images/")
    description = models.TextField()
    datetime = models.DateTimeField(default=timezone.now())


class Article(models.Model):
    image = models.ImageField(upload_to="images/", blank=True , null=True)
    title = models.TextField()
    body = models.TextField()
    datetime = models.DateTimeField(default=timezone.now())

