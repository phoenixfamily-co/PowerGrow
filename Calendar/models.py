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
    name = models.CharField(unique=True, blank=True, null=True, max_length=20)
    number = models.IntegerField(blank=True, null=True)
    startDay = models.CharField(blank=True, null=True, max_length=20)
    max = models.IntegerField(blank=True, null=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='months', null=True, blank=True)


class Day(models.Model):
    number = models.IntegerField(blank=True, null=True)
    name = models.CharField(blank=True, null=True, max_length=20)
    description = models.TextField(blank=True, null=True)
    holiday = models.BooleanField(blank=True, null=True)
    month = models.ForeignKey(Month, on_delete=models.CASCADE, related_name='days', null=True, blank=True)


class Time(models.Model):
    time = models.TimeField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    reserved = models.BooleanField(blank=True, null=True)
    price = models.IntegerField(default=695000)
    off = models.IntegerField(default=0)
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='times', null=True, blank=True)
