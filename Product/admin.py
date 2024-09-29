from django.contrib import admin
from .models import *


class ParticipantsAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']


admin.site.register(Participants, ParticipantsAdmin)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'sport')  # نمایش عنوان و ورزش در لیست


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ('title',)  # نمایش نام ورزش در لیست
