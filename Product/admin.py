from django.contrib import admin


from .models import *

admin.site.register(Course)
admin.site.register(Days)
admin.site.register(Sport)
admin.site.register(Sessions)


class ParticipantsAdmin(admin.ModelAdmin):
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if 'autocomplete' in request.path:
            branch_code = request.session['branch']
            queryset = queryset.filter(branch_code=branch_code)
        return queryset, use_distinct


admin.site.register(Participants, ParticipantsAdmin)

