from django.db import models

from Calendar.models import Day
from Product.models import Course

NEWS_CHOICE = (
    ('کنسلی', 'کنسلی'),
    ('تعطیل', 'تعطیل'),
    ('بقیه', 'بقیه'),
)


class News(models.Model):
    title = models.CharField(max_length=100, choices=NEWS_CHOICE, default='public', verbose_name="موضوع")
    date = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='news', null=True, blank=True, verbose_name="تاریخ")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='news', null=True, blank=True, verbose_name="دوره")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
