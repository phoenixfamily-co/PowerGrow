from django.db import models

from Calendar.models import Day
from Product.models import Course
from User.models import User

NEWS_CHOICE = (
    ('کنسلی', 'کنسلی'),
    ('تعطیل', 'تعطیل'),
    ('فنی', 'فنی'),
    ('غیره', 'غیره'),
)


class News(models.Model):
    title = models.CharField(max_length=100, choices=NEWS_CHOICE, default='public', verbose_name="موضوع")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")

    date = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='news', null=True, blank=True, verbose_name="تاریخ")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='news', null=True, blank=True,
                               verbose_name="دوره")
    created_at = models.DateTimeField(auto_now_add=True)
    users_who_read = models.ManyToManyField(User, related_name='read_news', blank=True)

    def is_new_for_user(self, user):
        return user not in self.users_who_read.all()
