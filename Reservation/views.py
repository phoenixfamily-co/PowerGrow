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

    # def get_queryset(self):
    #     queryset = Reservations.objects.filter(user=self.request.user.id)
    #     return queryset

    def perform_create(self, serializer):
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
                reservations, created = Reservations.objects.update_or_create(
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
                return Response({'redirect': ZP_API_STARTPAY + str(response['Authority'])})
            else:
                return Response({'error': 'Payment request failed'})
        except json.JSONDecodeError:
            return Response({'error': 'Failed to decode response JSON'})
        except KeyError:
            return Response({'error': 'Missing expected key in response JSON'})


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


def verify(request):
    reservation = Reservations.objects.get(authority=request.GET.get('Authority', ''))
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
        reservation.success = True
        reservation.time.reserved = True
        reservation.time.save()
        reservation.save()
        return JsonResponse({'status': True, 'RefID': response['RefID']})
    else:
        reservation.delete()
        return JsonResponse({'status': False, 'code': str(response['Status'])})
