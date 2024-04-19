from .models import *
from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    search_fields = ('name', 'number')
    list_display = ('name', 'number')


admin.site.register(User, UserAdmin)
