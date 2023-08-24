from django.db import models


# Create your models here.

class Slider(models.Model):
    image = models.ImageField(upload_to="media/images")
    description = models.TextField()


class Article(models.Model):
    image = models.ImageField(upload_to="media/images")
    title = models.TextField()
    body = models.TextField()
