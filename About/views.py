from django.http import HttpResponse
from django.template import loader
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from Product.models import Sport
from .serializer import *

from About.models import AboutUs


@cache_page(60 * 15)
def about_view(request):
    about = AboutUs.objects.values().first()
    sport = Sport.objects.all().values()
    template = loader.get_template('public/about.html')
    context = {
        "about" : about,
        "sport": sport,

    }
    return HttpResponse(template.render(context, request))


class About(viewsets.ModelViewSet):
    queryset = AboutUs.objects.all()
    serializer_class = AboutSerializer

    def create(self, request, *args, **kwargs):
        AboutUs.objects.all().delete()
        return super().create(request)
