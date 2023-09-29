from django.http import HttpResponse
from django.template import loader
from rest_framework import viewsets

from About.models import AboutUs
from Product.models import Sport
from Reservation.models import *
from Reservation.serializer import GymSerializer, ReservationSerializer, DatesSerializer, TimesSerializer


def reservation_view(request):
    about = AboutUs.objects.values().first()
    reservation = Gym.objects.values().first()
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
        "reservation" : reservation,
        "sport": sport,


    }
    return HttpResponse(template.render(context, request))


class GymView(viewsets.ModelViewSet):
    queryset = Gym.objects.all().first()
    serializer_class = GymSerializer

    def create(self, request, *args, **kwargs):
        Gym.objects.all().delete()
        return super().create(request)


class ReservationView(viewsets.ModelViewSet):
    queryset = Reservations.objects.all()
    serializer_class = ReservationSerializer
    # permission_classes = [IsAuthenticated]


class DateView(viewsets.ModelViewSet):
    queryset = Dates.objects.all()
    serializer_class = DatesSerializer


class TimeView(viewsets.ModelViewSet):
    queryset = Times.objects.all()
    serializer_class = TimesSerializer
