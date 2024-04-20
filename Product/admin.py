from django.contrib import admin
from .models import *


class ParticipantsAdmin(admin.ModelAdmin):
    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['user'].queryset = User.objects.filter(name__iexact='participants')
        return super(ParticipantsAdmin, self).render_change_form(request, context, *args, **kwargs)


admin.site.register(Participants, ParticipantsAdmin)
