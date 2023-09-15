from django.http import HttpResponse
from django.template import loader
from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializer import *


from About.models import AboutUs


def about_view(request):
    about = AboutUs.objects.values().first()
    template = loader.get_template('about.html')
    context = {
        "instagram": about["instagram"],
        "telegram": about["telegram"],
        "telephone": about["telephone"],
        "phone": about["phone"],
        "logo": about["logo"],
        "transparent_logo": about["transparent_logo"],
        "address": about["address"],
        "latitude": about["latitude"],
        "longitude": about["longitude"],
    }
    return HttpResponse(template.render(context, request))


class ChangeInfo(viewsets.ModelViewSet):
    queryset = AboutUs.objects.all()
    serializer_class = AboutSerializer

    def create(self, request, *args, **kwargs):
        telegram = request.data["telegram"]
        instagram = request.data["instagram"]
        telephone = request.data["telephone"]
        phone = request.data["phone"]
        logo = request.data["logo"]
        address = request.data["address"]
        transparent_logo = request.data["transparent_logo"]
        latitude = request.data["latitude"]
        longitude = request.data["longitude"]
        AboutUs.objects.all().delete()
        AboutUs.objects.create(telegram=telegram, instagram=instagram, telephone=telephone, phone=phone, logo=logo,
                               address=address, transparent_logo=transparent_logo, latitude=latitude,
                               longitude=longitude)
        return Response(status=status.HTTP_201_CREATED)
