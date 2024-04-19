from django.contrib import admin
from Product.models import *

admin.site.register(Course)
admin.site.register(Days)
admin.site.register(Sport)
admin.site.register(Participants)


class QuestionAdmin(admin.ModelAdmin):
    ordering = ['date_created']
    search_fields = ["user__number"]