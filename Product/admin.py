from django.contrib import admin
from .models import *


class ParticipantsAdmin(admin.ModelAdmin):
    model = Participants
    autocomplete_fields = ['user']


admin.site.register(Participants, ParticipantsAdmin)
