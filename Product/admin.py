from django.contrib import admin
from .models import *


@admin.register(Participants)
class ParticipantsAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    list_display = ('name', 'user')
    list_filter = ('user__name',)


