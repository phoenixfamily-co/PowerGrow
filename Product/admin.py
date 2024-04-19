from django.contrib import admin


from .models import *

admin.site.register(Course)
admin.site.register(Days)
admin.site.register(Sport)
admin.site.register(Sessions)


class ParticipantsAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']


admin.site.register(Participants, ParticipantsAdmin)

