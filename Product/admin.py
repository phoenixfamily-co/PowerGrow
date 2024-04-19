from Product.models import *
from django.contrib import admin


admin.site.register(Course)
admin.site.register(Days)
admin.site.register(Sport)


class ParticipantsAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    list_display = ['user']


admin.site.register(Participants, ParticipantsAdmin)
