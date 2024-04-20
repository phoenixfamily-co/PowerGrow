from django.contrib import admin
from .models import *


@admin.register(Participants)
class ParticipantsAdmin(admin.ModelAdmin):
    model = Participants
    autocomplete_fields = ['user']


