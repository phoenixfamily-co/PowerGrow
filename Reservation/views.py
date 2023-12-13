from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import redirect
from django.template import loader
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from About.models import AboutUs
from Product.models import Sport
from Reservation.models import *
from Reservation.serializer import GymSerializer, ReservationSerializer, AdminReservationSerializer
from django.conf import settings
import requests
import json

if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
description = "رزرو سالن چند منظور حجاب"  # Required
phone = 'YOUR_PHONE_NUMBER'  # Optional
# Important: need to edit for realy server.
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
    reserve = Reservations.objects.all()
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
    reserve = Reservations.objects.all()
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
    reserves = Reservations.objects.filter(user=pk).all()

    context = {
        "about": about,
        "reserves": reserves,
    }
    return HttpResponse(template.render(context, request))


class GymView(viewsets.ModelViewSet):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer


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
        time.reserved = True
        time.save()
        reservations = Reservations.objects.update_or_create(title=data["title"],
                                                             description=data["description"],
                                                             time=time,
                                                             holiday=bool(data["holiday"]),
                                                             session=data["session"],
                                                             price=data["price"],
                                                             gym=gym)
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


def send_request(request, amount, time, holiday, session, gym):
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount,
        "mobile": phone,
        "Description": description,
        "CallbackURL": CallbackURL,
        "metadata": {
            "time": time,
            "holiday": holiday,
            "session": session,
            "gym": gym,
        }
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return redirect(ZP_API_STARTPAY + str(response['Authority']))

            else:
                return JsonResponse({'status': False, 'code': str(response['Status'])})
        return JsonResponse(response)

    except requests.exceptions.Timeout:
        return JsonResponse({'status': False, 'code': 'timeout'})
    except requests.exceptions.ConnectionError:
        return JsonResponse({'status': False, 'code': 'connection error'})


def verify(request):
    authority_data = {
        "MerchantID": settings.MERCHANT,
        "Authority": request.GET.get('Authority', ''),
        "Amount": 695000
    }

    data = json.dumps(authority_data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
    response_data = response.json()

    # if request.GET.get('OK') == 'OK':
    #     response_data = response.json()
    #     if response_data['Status'] == 100:
    #         return JsonResponse({'status': True})
    #     else:
    #         return JsonResponse({'status': False})

    return JsonResponse(response_data)
