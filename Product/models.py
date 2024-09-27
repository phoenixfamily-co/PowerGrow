from django.db import models
from django.utils import timezone

from Calendar.models import Day
from PowerGrow import settings
from User.models import User

TYPE_CHOICE = (
    ('خصوصی', 'private'),
    ('نیمه خصوصی', 'semiprivate'),
    ('عمومی', 'public')
)
GENDER_CHOICE = (
    ('آقایان', 'men'),
    ('بانوان', 'women'),
)


class Sport(models.Model):
    title = models.CharField(max_length=50)


class Course(models.Model):
    title = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, choices=TYPE_CHOICE, default='public')
    time = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    selected = models.BooleanField(default=False, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE)
    datetime = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='courses', null=True, blank=True)


class Session(models.Model):
    number = models.IntegerField(blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, related_name='sessions', null=True, blank=True)


class Days(models.Model):
    title = models.TextField(blank=True, null=True)
    tuition = models.IntegerField()
    off = models.IntegerField(blank=True, null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='days', null=True, blank=True)


class Participants(models.Model):
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='participants', null=True, blank=True)
    day = models.ForeignKey(Days, on_delete=models.CASCADE, related_name='participants', null=True, blank=True)
    price = models.IntegerField(default=0)
    datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participants',
                             blank=True, null=True)

    startDay = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='participants',
                                 blank=True, null=True)

    endDay = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='end_participants',
                               blank=True, null=True)

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='participants', null=True, blank=True)
    created = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='participant',
                                blank=True, null=True)
    authority = models.TextField(unique=True, blank=True, null=True)
    success = models.BooleanField(blank=True, null=True)
