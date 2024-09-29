from django.contrib import admin
from .models import *


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'sport')  # نمایش عنوان و ورزش در لیست


@admin.register(Days)
class DaysAdmin(admin.ModelAdmin):
    list_display = ('title', 'tuition', 'off', 'session')  # یا فیلدهای دیگری که می‌خواهی نمایش بدهی
    search_fields = ('title',)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('number', 'course')
    search_fields = ('number',)


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ('title',)  # نمایش نام ورزش در لیست


@admin.register(Participants)
class ParticipantsAdmin(admin.ModelAdmin):
    list_display = ('title', 'day', 'session', 'startDay', 'endDay', 'user', 'course')
    autocomplete_fields = ('day', 'user')  # اضافه کردن قابلیت autocomplete برای فیلد day

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if 'course' in request.GET:  # اگر دوره‌ای در GET وجود داشته باشد
            course_id = request.GET['course']
            form.base_fields['day'].queryset = Days.objects.filter(session__course_id=course_id)
            form.base_fields['session'].queryset = Session.objects.filter(course_id=course_id)
        else:  # در غیر این صورت، هیچ روز یا جلسه‌ای را نمایش نده
            form.base_fields['day'].queryset = Days.objects.none()
            form.base_fields['session'].queryset = Session.objects.none()

        return form


