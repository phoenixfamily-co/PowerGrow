from rest_framework import viewsets, status
from rest_framework.response import Response

from Product.models import Course, Sport
from About.models import AboutUs
from django.template import loader
from .serializer import *
from django.http import HttpResponse, Http404


def home_view(request):
    images = Slider.objects.all().order_by("datetime").values()
    selected = Course.objects.filter(selected=True).order_by("datetime").values()
    about = AboutUs.objects.values().first()
    sport = Sport.objects.all().values()
    template = loader.get_template('public/home.html')
    context = {
        "images": images,
        "selected": selected,
        "about": about,
        "sport": sport,

    }
    return HttpResponse(template.render(context, request))


class SliderView(viewsets.ModelViewSet):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

