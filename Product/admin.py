from django.contrib import admin
from .models import *


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'sport')  # نمایش عنوان و ورزش در لیست


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ('title',)  # نمایش نام ورزش در لیست


@admin.register(Participants)
class ParticipantsAdmin(admin.ModelAdmin):
    list_display = ('title', 'day')  # اینجا نمایش عنوان و روز
    autocomplete_fields = ('day',)  # اضافه کردن قابلیت autocomplete برای فیلد day

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "day":
            kwargs["queryset"] = Day.objects.all().order_by('-id')  # مرتب‌سازی بر اساس ID
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


