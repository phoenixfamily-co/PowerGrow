from django.contrib import admin

from Calendar.models import *

admin.site.register(Year)
admin.site.register(Month)
admin.site.register(Day)
admin.site.register(Time)
