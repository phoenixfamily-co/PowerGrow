from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from Product.models import Course, Sport
from About.models import AboutUs
from django.template import loader
from .serializer import *
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from PowerGrow.permissions import *


@cache_page(60 * 15)
@csrf_exempt
def home_view(request):
    images = Slider.objects.all().order_by("datetime").values()
    selected = Course.objects.filter(selected=True, active=True).order_by("datetime").values()
    newDay = Course.objects.filter(newDay=True, active=True).order_by("datetime").values()[:6]
    about = AboutUs.objects.values().first()
    sport = Sport.objects.all().values()
    template = loader.get_template('public/home.html')
    context = {
        "images": images,
        "first": images.first(),
        "selected": selected,
        "about": about,
        "sport": sport,
        "newDay": newDay,

    }
    return HttpResponse(template.render(context, request))


@cache_page(60 * 15)
@csrf_exempt
def slider_view(request):
    about = AboutUs.objects.values().first()
    slider = Slider.objects.all().values()
    template = loader.get_template('manager/banners.html')
    context = {
        "slider": slider,
        "about": about,
    }
    return HttpResponse(template.render(context, request))


class SliderView(viewsets.ModelViewSet):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    permission_classes = [IsAdminUserOrStaff]
