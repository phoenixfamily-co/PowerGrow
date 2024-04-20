from django.contrib import admin
from admin_auto_filters.filters import AutocompleteFilter
from .models import *


class ParticipantsFilter(AutocompleteFilter):
    title = 'User'  # display title
    field_name = 'user'  # name of the foreign key field


class ParticipantsAdmin(admin.ModelAdmin):
    list_filter = [ParticipantsFilter]


admin.site.register(Participants, ParticipantsAdmin)
admin.site.register(User)
