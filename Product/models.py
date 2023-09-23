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


class Course(models.Model):
    title = models.CharField(max_length=60)
    name = models.CharField(max_length=60)
    type = models.CharField(max_length=60, choices=TYPE_CHOICE, default='public')
    time = models.CharField(max_length=50)
    session = models.IntegerField()
    tuition = models.IntegerField()
    off = models.IntegerField(null=True,blank=True)
    price = models.IntegerField(default=0)
    description = models.TextField()
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    profile = models.ImageField(upload_to="images/", blank=True, null=True)
    selected = models.BooleanField()
    capacity = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE)
    start = models.DateField(null=True,blank=True)
    datetime = models.DateTimeField(default=timezone.now)


class Days(models.Model):
    day = models.TextField(blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='days', null=True, blank=True)
