from django.utils import timezone

from PowerGrow import settings
from User.models import User
from Calendar.models import *


class Gym(models.Model):
    title = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    off = models.IntegerField(default=0, blank=True, null=True)
    tuition = models.IntegerField()
    contract = models.FileField(upload_to="files/", blank=True, null=True)
    datetime = models.DateTimeField(default=timezone.now)


class Reservations(models.Model):
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    time = models.ForeignKey(Time, on_delete=models.CASCADE, related_name='reservations', blank=True, null=True)
    holiday = models.BooleanField(blank=True, null=True)
    session = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    datetime = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations',
                             blank=True, null=True)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='reservations', null=True, blank=True)
    created = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservation',
                                blank=True, null=True)
