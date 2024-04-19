from Product.models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Participants
admin.site.register(Course)
admin.site.register(Days)
admin.site.register(Sport)

# UserAdmin.search_fields = ('name', 'number')


class ParticipantsAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']


admin.site.unregister(User)
admin.site.register(Participants, ParticipantsAdmin)
admin.site.register(User, UserAdmin)

