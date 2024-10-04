from django.db import models

TYPE_CALENDAR = (
    ('جلالی', 'Jalali'),
    ('میلادی', 'Gregorian'),
    ('قمری', 'Lunar')
)


class Year(models.Model):
    number = models.IntegerField(unique=True, null=True, blank=True)
    name = models.CharField(blank=True, null=True, max_length=20, choices=TYPE_CALENDAR)
    leap = models.BooleanField(blank=True, null=True)


class Month(models.Model):
    name = models.CharField(blank=True, null=True, max_length=20)
    number = models.IntegerField(blank=True, null=True)
    startDay = models.CharField(blank=True, null=True, max_length=20)
    max = models.IntegerField(blank=True, null=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='months', null=True, blank=True)

    def __str__(self):
        # فرض بر این است که شماره روز و شماره ماه و سال را می‌خواهیم نمایش دهیم
        year = self.year.number if self and self.year else "Unknown Year"
        return f"{year}-{self.name}"  # به فرمت YYYY/MM/DD


class Day(models.Model):
    number = models.IntegerField(blank=True, null=True, verbose_name="شماره روز")
    name = models.CharField(blank=True, null=True, max_length=20, verbose_name="نام روز در هفته")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات مناسبت")
    holiday = models.BooleanField(blank=True, null=True,  verbose_name="تعطیلات")
    month = models.ForeignKey(Month, on_delete=models.CASCADE, related_name='days', null=True, blank=True,
                              verbose_name="ماه")

    def __str__(self):
        # فرض بر این است که شماره روز و شماره ماه و سال را می‌خواهیم نمایش دهیم
        year = self.month.year.number if self.month and self.month.year else "Unknown Year"
        return f"{year}/{self.month.number}/{self.number}"  # به فرمت YYYY/MM/DD


class Time(models.Model):
    time = models.TimeField(blank=True, null=True, verbose_name="زمان")
    duration = models.IntegerField(blank=True, null=True, verbose_name="مدت به دقیقه")
    reserved = models.BooleanField(blank=True, null=True,verbose_name="رزرو شده")
    res_id = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(default=695000, verbose_name="قیمت")
    off = models.IntegerField(default=0, verbose_name="تخفیف")
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='times', null=True, blank=True, verbose_name="تاریخ")

    def __str__(self):
        # فرض بر این است که شماره روز و شماره ماه و سال را می‌خواهیم نمایش دهیم
        year = self.day.month.year.number if self.day.month else "Unknown Year"
        return f"{year}/{self.day.month.number}/{self.day.number} : {self.time}"  # به فرمت YYYY/MM/DD
