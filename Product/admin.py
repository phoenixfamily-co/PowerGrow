from django.contrib import admin
from .models import *


@admin.register(Participants)
class ParticipantsAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('user__name',)


