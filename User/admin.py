from django.contrib import admin
from User.models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.register(User)

UserAdmin.search_fields = ('name', 'number')


