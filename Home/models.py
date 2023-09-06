from django.db import models


# Create your models here.

class Slider(models.Model):
    image = models.ImageField(upload_to="images/")
    description = models.TextField()


class Article(models.Model):
    image = models.ImageField(upload_to="images/", blank=True , null=True)
    title = models.TextField()
    body = models.TextField()
