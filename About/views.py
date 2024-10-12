from django.http import HttpResponse
from django.template import loader
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from Product.models import Sport
from .serializer import *

from About.models import AboutUs


@cache_page(60 * 15)
@csrf_exempt
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
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        AboutUs.objects.all().delete()
        return super().create(request)
