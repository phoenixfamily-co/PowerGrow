from django.db import models
from django.utils import timezone

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
    title = models.CharField(max_length=60)
    name = models.CharField(max_length=60)
    type = models.CharField(max_length=60, choices=TYPE_CHOICE, default='public')
    time = models.CharField(max_length=50)
    tuition = models.IntegerField()
    off = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    profile = models.ImageField(upload_to="images/", blank=True, null=True)
    selected = models.BooleanField()
    capacity = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE)
    start = models.DateField(null=True,blank=True)
    datetime = models.DateTimeField(default=timezone.now)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='course', null=True, blank=True)


class Days(models.Model):
    day = models.TextField(blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='days', null=True, blank=True)


class Sessions(models.Model):
    session = models.IntegerField(blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sessions', null=True, blank=True)
