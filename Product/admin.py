from django.contrib import admin
from admin_auto_filters.filters import AutocompleteFilter


class ParticipantsFilter(AutocompleteFilter):
    title = 'User'  # display title
    field_name = 'user'  # name of the foreign key field


class UserAdmin(admin.ModelAdmin):
    search_fields = ('name', 'number')  # this is required for django's autocomplete functionality


class ParticipantsAdmin(admin.ModelAdmin):
    list_filter = [ParticipantsFilter]
