from django.contrib import admin
from .models import *


@admin.register(Participants)
class ParticipantsAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']


