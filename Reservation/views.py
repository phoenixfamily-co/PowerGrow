from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from About.models import AboutUs


def reservation_view(request):
    about = AboutUs.objects.values().first()
    template = loader.get_template('public/reservation.html')
    context = {
        "logo": about["logo"],
    }
    return HttpResponse(template.render(context, request))
