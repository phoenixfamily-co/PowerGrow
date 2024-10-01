from django.db import models
from django.utils import timezone

from Calendar.models import Day
from PowerGrow import settings
from User.models import User

TYPE_CHOICE = [
    ('public', 'عمومی'),
    ('private', 'خصوصی'),
    ('semi_private', 'نیمه خصوصی'),  # گزینه جدید
]
GENDER_CHOICE = [
    ('male', 'مرد'),
    ('female', 'زن'),
]


class Sport(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title  # به جای ID، نام ورزش را نمایش می‌دهد


class Course(models.Model):
    title = models.TextField(blank=True, null=True, verbose_name='عنوان')
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='نام مربی')
    type = models.CharField(max_length=100, choices=TYPE_CHOICE, default='public', verbose_name='نوع دوره')
    time = models.TextField(blank=True, null=True,verbose_name='زمان')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    image = models.ImageField(upload_to="images/", blank=True, null=True, verbose_name='تصویر')
    selected = models.BooleanField(default=False, blank=True, null=True, verbose_name='منتخب')
    capacity = models.IntegerField(blank=True, null=True, verbose_name='ظرفیت')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE, verbose_name='جنسیت')
    datetime = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(blank=True, null=True, verbose_name='فعال')
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='courses', null=True, blank=True,
                              verbose_name='ورزش')

    def __str__(self):
        return f"{self.pk}-{self.title}"  # به جای ID، نام ورزش را نمایش می‌دهد


class Session(models.Model):
    number = models.IntegerField(blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, related_name='sessions', null=True, blank=True)

    def __str__(self):
        return f"{self.number} جلسه {self.course}"


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
