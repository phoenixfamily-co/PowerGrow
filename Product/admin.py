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
    list_display = ('title', 'day', 'session', 'startDay', 'endDay', 'user', 'course')  # اینجا نمایش عنوان و روز
    autocomplete_fields = ('day', 'user')  # اضافه کردن قابلیت autocomplete برای فیلد day

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "startDay":
            kwargs["queryset"] = Day.objects.all().order_by('-id')  # مرتب‌سازی بر اساس ID
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'course' in request.GET:
            course_id = request.GET['course']
            # فقط روزها و جلسات مرتبط با دوره خاص را نشان می‌دهد
            form.base_fields['day'].queryset = Day.objects.filter(course_id=course_id)
            form.base_fields['session'].queryset = Session.objects.filter(course_id=course_id)
        return form


admin.site.register(Participants, ParticipantsAdmin)



