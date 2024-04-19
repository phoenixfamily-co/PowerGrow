from django.contrib import admin
from django.contrib.auth.models import User


@admin.register(User)
class ParticipantsAdmin(admin.ModelAdmin):
    list_display = ('name', 'number')
    search_fields = ('name', 'number')

