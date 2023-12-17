from django.http import HttpResponse, Http404
from django.template import loader
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from About.models import AboutUs
from Product.models import Sport
from Reservation.models import *
from Reservation.serializer import GymSerializer, ReservationSerializer, AdminReservationSerializer
from django.conf import settings
import requests
import json
from django.core import serializers

if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
CallbackURL = 'https://powergrow.net/reservation/verify/'


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


def gym_view(request):
    about = AboutUs.objects.values().first()
    gym = Gym.objects.all()
    template = loader.get_template('manager/gym.html')
    context = {
        "about": about,
        "gym": gym,
    }
    return HttpResponse(template.render(context, request))


def admin_gym_view(request):
    about = AboutUs.objects.values().first()
    gym = Gym.objects.all()
    template = loader.get_template('secretary/gyms.html')
    context = {
        "about": about,
        "gym": gym,
    }
    return HttpResponse(template.render(context, request))


def reserve_view(request):
    about = AboutUs.objects.values().first()
    reserve = Reservations.objects.filter(success=True).all()
    gym = Gym.objects.all().first()
    template = loader.get_template('manager/reserves.html')
    context = {
        "about": about,
        "reserve": reserve,
        "gym": gym,
    }
    return HttpResponse(template.render(context, request))


def admin_reserve_view(request):
    about = AboutUs.objects.values().first()
    reserve = Reservations.objects.filter(success=True).all()
    gym = Gym.objects.all().first()
    template = loader.get_template('secretary/reserves.html')
    context = {
        "about": about,
        "reserve": reserve,
        "gym": gym,
    }
    return HttpResponse(template.render(context, request))


def user_reserves_view(request, pk):
    template = loader.get_template('user/reserves.html')
    about = AboutUs.objects.values().first()
    reserves = Reservations.objects.filter(user=pk, success=True).all()

    context = {
        "about": about,
        "reserves": reserves,
    }
    return HttpResponse(template.render(context, request))


class GymView(viewsets.ModelViewSet):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer


class ReservationView(viewsets.ViewSet):
    queryset = Reservations.objects.all()
    serializer_class = ReservationSerializer

    def list(self, serializer):
        queryset = Reservations.objects.filter(user=self.request.user.id)
        return queryset

    def create(self, serializer):
        data = self.request.data
        authority_data = {
            "MerchantID": settings.MERCHANT,
            "Amount": data["price"],
            "phone": str(self.request.user.number),
            "Description": data["description"],
            "CallbackURL": CallbackURL,
        }
        authority_data = json.dumps(authority_data)
        headers = {'content-type': 'application/json', 'content-length': str(len(authority_data))}
        response = requests.post(ZP_API_REQUEST, data=authority_data, headers=headers, timeout=10)

        try:
            response_data = response.json()  # Parse the response content as JSON
            if response_data['Status'] == 100:
                gym = Gym.objects.filter(id=data["gym"]).first()
                time = Time.objects.filter(id=data["time"]).first()
                Reservations.objects.update_or_create(
                    title=data["title"],
                    description=data["description"],
                    time=time,
                    holiday=bool(data["holiday"]),
                    session=data["session"],
                    price=data["price"],
                    gym=gym,
                    user=self.request.user,
                    authority=str(response_data['Authority']),
                    success=False
                )
                return Response({'payment': ZP_API_STARTPAY, 'authority': str(response_data['Authority'])},
                                status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Payment request failed'}, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return Response({'error': 'Failed to decode response JSON'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'error': 'Missing expected key in response JSON'}, status=status.HTTP_400_BAD_REQUEST)


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
                                                             success=True,
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


@api_view(('GET',))
def verify(request):
    reservation = Reservations.objects.get(authority=request.GET.get('Authority', ''))
    about = AboutUs.objects.values().first()
    sport = Sport.objects.all().values()

    context = {
        "about": about,
        "sport": sport,
        "reservation": reservation
    }

    authority_data = {
        "MerchantID": settings.MERCHANT,
        "Authority": reservation.authority,
        "Amount": reservation.price
    }

    data = json.dumps(authority_data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
    response = response.json()
    if response['Status'] == 100:
        template = loader.get_template('public/successful.html')
        reservation.success = True
        sliced_queryset = Time.objects.filter(day__name=reservation.time.day.name, time=reservation.time.time,
                                              day__number__gte=reservation.time.day.number,
                                              day__month__number__gte=reservation.time.day.month.number).order_by(
            'day__number').order_by('day__month__number')[:int(reservation.session)]
        # time = Time.objects.filter(id__in=sliced_queryset).update(reserved=True)
        reservation.save()
        return Response(sliced_queryset.values())
        # return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('public/failed.html')
        reservation.time.reserved = False
        reservation.time.save()
        reservation.delete()
        return HttpResponse(template.render(context, request))
