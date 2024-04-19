from django.contrib import admin
from User.models import *

admin.site.register(User)


class QuestionAdmin(admin.ModelAdmin):
    ordering = ['date_created']
    search_fields = ["user__number"]

