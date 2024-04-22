from django.contrib import admin
from .models import *


class ParticipantsAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']


admin.site.register(Participants, ParticipantsAdmin)
