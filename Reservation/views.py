from django.http import HttpResponse
from django.template import loader

from About.models import AboutUs
from Product.models import Sport


def reservation_view(request):
    about = AboutUs.objects.values().first()
    sport = Sport.objects.all().values()

    template = loader.get_template('public/reservation.html')
    context = {
        "logo": about["logo"],
        "instagram": about["instagram"],
        "telegram": about["telegram"],
        "telephone": about["telephone"],
        "phone": about["phone"],
        "transparent_logo": about["transparent_logo"],
        "address": about["address"],
        "latitude": about["latitude"],
        "longitude": about["longitude"],
        "sport": sport,

    }
    return HttpResponse(template.render(context, request))
