from django.db import models
from django.utils import timezone

from User.models import User


class Gym(models.Model):
    title = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    off = models.IntegerField(default=0, blank=True, null=True)
    tuition = models.IntegerField()
    contract = models.FileField(upload_to="files/", blank=True, null=True)


class Reservations(models.Model):
    title = models.TextField(blank=True, null=True)
    startDate = models.DateField(blank=True, null=True)
    endDate = models.DateField(blank=True, null=True)
    startTime = models.TimeField(blank=True, null=True)
    endTime = models.TimeField(blank=True, null=True)
    session = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    datetime = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='reservations', null=True, blank=True)


class Dates(models.Model):
    reserved = models.BooleanField(blank=True, null=True)
    date = models.DateField(default=False, blank=True, null=True)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='dates', null=True, blank=True)


class Times(models.Model):
    reserved = models.BooleanField(blank=True, null=True)
    time = models.TimeField(default=False, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    date = models.ForeignKey(Dates, on_delete=models.CASCADE, related_name='times', null=True, blank=True)
