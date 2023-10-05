import json

from django.http import HttpResponse
from django.template import loader
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from Calendar.models import *

from About.models import AboutUs
from Product.models import Sport
from Reservation.models import *
from Reservation.serializer import GymSerializer, ReservationSerializer, DatesSerializer, TimesSerializer


def reservation_view(request):
    about = AboutUs.objects.values().first()
    gym = Gym.objects.values().first()
    sport = Sport.objects.all().values()
    year = Year.objects.all().values().first().prefetch_related('month')
    month = Month.objects.get(id=3)
    day = Day.objects.filter(month=3).values()
    template = loader.get_template('public/reservation.html')
    context = {
        "about": about,
        "gym" : gym,
        "sport": sport,
        "year": year,
        "month": month,
        "day": day,
    }
    return HttpResponse(template.render(context, request))


def transaction_view(request, pk, start, end, session):
    about = AboutUs.objects.values().first()
    gym = Gym.objects.filter(id=pk).values().first()
    sport = Sport.objects.all().values()
    template = loader.get_template('public/transaction.html')
    context = {
        "about": about,
        "gym" : gym,
        "sport": sport,
        "start": start,
        "end": end,
        "session": session
    }
    return HttpResponse(template.render(context, request))


def successful_view(request,  pk, start, end, session):
    about = AboutUs.objects.values().first()
    gym = Gym.objects.filter(id=pk).values().first()
    sport = Sport.objects.all().values()
    template = loader.get_template('public/sucessful.html')
    context = {
        "about": about,
        "gym": gym,
        "sport": sport,
        "start": start,
        "end": end,
        "session": session
    }

    return HttpResponse(template.render(context, request))


class GymView(viewsets.ModelViewSet):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer

    def get_queryset(self):
        return Gym.objects.values().first()

    def create(self, request, *args, **kwargs):
        Gym.objects.all().delete()
        return super().create(request)


class ReservationView(viewsets.ModelViewSet):
    queryset = Reservations.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Reservations.objects.filter(user=self.request.user.id)
        return queryset

    def perform_create(self, serializer):
        data = self.request.data
        gym = Gym.objects.get(id=data["course"])
        reservations = Reservations.objects.update_or_create(title=data["title"],
                                                             startDateTime=data["start"],
                                                             endDateTime=data["end"],
                                                             reserved=data["reserved"],
                                                             session=data["session"],
                                                             price=data["price"],
                                                             user=self.request.user,
                                                             gym=gym)
        serializer = ReservationSerializer(reservations)
        return Response(serializer.data)


class DateView(viewsets.ModelViewSet):
    queryset = Dates.objects.all()
    serializer_class = DatesSerializer


class TimeView(viewsets.ModelViewSet):
    queryset = Times.objects.all()
    serializer_class = TimesSerializer
