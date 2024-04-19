from Product.models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.register(Course)
admin.site.register(Days)
admin.site.register(Sport)

admin.site.register(User, UserAdmin)


@admin.register(Participants)
class ParticipantsAdmin(admin.ModelAdmin):
    search_fields = ('name', 'number')


