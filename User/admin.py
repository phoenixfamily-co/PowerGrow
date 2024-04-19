from django.contrib import admin
from User.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'number')
    search_fields = ('name', 'number')


admin.site.register(User, UserAdmin)

