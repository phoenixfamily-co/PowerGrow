from django.http import HttpResponse, Http404
from django.template import loader
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from About.models import AboutUs
from Product.models import Sport
from Reservation.models import *
from Reservation.serializer import GymSerializer, ReservationSerializer, AdminReservationSerializer


def reservation_view(request):
    about = AboutUs.objects.values().first()
    gym = Gym.objects.values().first()
    sport = Sport.objects.all().values()
    year = Year.objects.values().first()
    template = loader.get_template('public/reservation.html')
    context = {
        "about": about,
        "gym": gym,
        "sport": sport,
        "year": year,
    }
    return HttpResponse(template.render(context, request))


def transaction_view(request, gym, time, session, holiday):
    about = AboutUs.objects.values().first()
    gym = Gym.objects.filter(id=gym).values().first()
    times = Time.objects.get(id=time)
    sport = Sport.objects.all().values()
    template = loader.get_template('public/transaction.html')
    context = {
        "about": about,
        "gym": gym,
        "sport": sport,
        "time": times,
        "holiday": holiday,
        "session": session,
    }
    return HttpResponse(template.render(context, request))


def successful_view(request, gym, time, session, holiday):
    about = AboutUs.objects.values().first()
    gym = Gym.objects.filter(id=gym).values().first()
    times = Time.objects.get(id=time)
    sport = Sport.objects.all().values()
    template = loader.get_template('public/successful.html')
    context = {
        "about": about,
        "gym": gym,
        "sport": sport,
        "holiday": holiday,
        "time": times,
        "session": session,

    }

    return HttpResponse(template.render(context, request))


class GymView(viewsets.ModelViewSet):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer

    def create(self, request, *args, **kwargs):
        Gym.objects.all().delete()
        return super().create(request)


class ReservationView(viewsets.ModelViewSet):
    queryset = Reservations.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        queryset = Reservations.objects.filter(user=self.request.user.id)
        return queryset

    def perform_create(self, serializer):
        data = self.request.data
        gym = Gym.objects.filter(id=data["gym"]).first()
        time = Time.objects.filter(id=data["time"]).first()
        user = User.objects.filter(id=self.request.user.id)
        time.reserved = True
        time.save()
        reservations = Reservations.objects.update_or_create(title=data["title"],
                                                             description=data["description"],
                                                             time=time,
                                                             holiday=data["holiday"],
                                                             session=data["session"],
                                                             price=data["price"],
                                                             user=user,
                                                             gym=gym,
                                                             created=self.request.user)
        serializer = ReservationSerializer(reservations)
        return Response(serializer.data)


class ManagerAddReservationView(viewsets.ModelViewSet):
    queryset = Reservations.objects.all()
    serializer_class = AdminReservationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'time'

    def get_queryset(self):
        data = self.kwargs
        queryset = self.queryset.filter(time=data['time'])
        return queryset

    def perform_create(self, serializer):
        data = self.request.data
        gym = Gym.objects.filter(id=data["gym"]).first()
        time = Time.objects.filter(id=self.kwargs['time']).first()
        time.reserved = True
        time.save()
        user = User.objects.filter(id=data["user"]).first()
        reservations = Reservations.objects.update_or_create(title=data["title"],
                                                             description=data["description"],
                                                             time=time,
                                                             holiday=bool(data["holiday"]),
                                                             session=data["session"],
                                                             price=data["price"],
                                                             user=user,
                                                             gym=gym,
                                                             created=self.request.user)
        serializer = ReservationSerializer(reservations)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        time = Time.objects.filter(id=self.kwargs['time']).first()
        time.reserved = False
        time.save()
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
