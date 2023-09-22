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
    day = models.CharField(max_length=100)
    type = models.CharField(max_length=60, choices=TYPE_CHOICE, default='public')
    time = models.CharField(max_length=50)
    session = models.IntegerField()
    tuition = models.IntegerField()
    off = models.IntegerField()
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to="images/")
    profile = models.ImageField(upload_to="images/")
    selected = models.BooleanField()
    capacity = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE)
    start = models.DateTimeField(default=timezone.now)
    datetime = models.DateTimeField(default=timezone.now)
