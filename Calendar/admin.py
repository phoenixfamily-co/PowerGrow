from django.contrib import admin

from Calendar.models import *


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ('name', 'number')
    search_fields = ('name',)  # یا هر فیلدی که می‌خواهی جستجو شود
    ordering = ('-id',)  # مرتب‌سازی بر اساس ID جدیدترین به قدیمی‌ترین
