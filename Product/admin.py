from django.contrib import admin
from .models import *


@admin.register(Participants)
class ParticipantsAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(name__in=['God', 'Demi God'])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


