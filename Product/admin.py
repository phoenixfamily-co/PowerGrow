from django.contrib import admin
from Product.models import *

admin.site.register(Course)
admin.site.register(Days)
admin.site.register(Sport)
admin.site.register(Participants)


# @admin.register(Participants)
# class ParticipantsAdmin(admin.ModelAdmin):
#     autocomplete_fields = ['user__number']
