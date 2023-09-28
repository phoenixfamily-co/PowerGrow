from rest_framework import viewsets
from Product.models import Course, Sport
from About.models import AboutUs
from django.template import loader
from .serializer import *
from django.http import HttpResponse


def home_view(request):
    images = Slider.objects.all().order_by("datetime").values()
    selected = Course.objects.filter(selected=True).order_by("datetime").values()
    course = Course.objects.get(selected=True)
    days = course.days.all()
    about = AboutUs.objects.values().first()
    sport = Sport.objects.all().values()
    template = loader.get_template('public/home.html')
    context = {
        "images": images,
        "selected": selected,
        "days": days,
        "instagram": about["instagram"],
        "telegram": about["telegram"],
        "telephone": about["telephone"],
        "phone": about["phone"],
        "logo": about["logo"],
        "transparent_logo": about["transparent_logo"],
        "address": about["address"],
        "latitude": about["latitude"],
        "longitude": about["longitude"],
        "sport": sport,

    }
    return HttpResponse(template.render(context, request))


class SliderView(viewsets.ModelViewSet):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer

