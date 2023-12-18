import requests
from django.http import HttpResponse
from django.template import loader
from rest_framework import viewsets, filters, generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from About.models import AboutUs
from User.models import *
from Product.serializer import *
from django.conf import settings
import json

if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
CallbackURL = 'https://powergrow.net/product/verify/'


def product_view(request, pk, session, day):
    about = AboutUs.objects.values().first()
    sport = Sport.objects.all().values()
    product = Course.objects.get(id=pk)
    participants = Participants.objects.filter(course__pk=pk).values()
    sessions = Sessions.objects.filter(id=session).values().first()
    days = Days.objects.filter(id=day).values().first()
    template = loader.get_template('public/product.html')
    context = {
        "about": about,
        "product": product,
        "participants": len(list(participants)),
        "session": sessions,
        "sport": sport,
        "day": days,

    }
    return HttpResponse(template.render(context, request))


def payment_view(request, pk, session, day):
    about = AboutUs.objects.values().first()
    product = Course.objects.filter(id=pk).values().first()
    sessions = Sessions.objects.filter(id=session).values().first()
    days = Days.objects.filter(id=day).values().first()
    template = loader.get_template('public/payment.html')
    context = {
        "about": about,
        "product": product,
        "session": sessions,
        "day": days,
    }
    return HttpResponse(template.render(context, request))


def check_view(request, pk, session, day):
    product = Course.objects.filter(id=pk).values().first()
    sessions = Sessions.objects.filter(id=session).values().first()
    days = Days.objects.filter(id=day).values().first()
    template = loader.get_template('public/check.html')
    context = {
        "product": product,
        "session": sessions,
        "days": days,

    }
    return HttpResponse(template.render(context, request))


def category_view(request, pk):
    template = loader.get_template('public/category.html')
    about = AboutUs.objects.values().first()
    sport = Sport.objects.all()
    course = Course.objects.all()
    context = {
        "about": about,
        "sport": sport,
        "selected": course.filter(sport=pk).values(),
        "title": sport.filter(id=pk).values().first(),
        "id": pk
    }
    return HttpResponse(template.render(context, request))


def sports_view(request):
    template = loader.get_template('manager/sports.html')
    sport = Sport.objects.all()
    about = AboutUs.objects.values().first()
    context = {
        "about": about,
        "sport": sport,
    }
    return HttpResponse(template.render(context, request))


def admin_sports_view(request):
    template = loader.get_template('secretary/sports.html')
    sport = Sport.objects.all()
    about = AboutUs.objects.values().first()
    context = {
        "about": about,
        "sport": sport,
    }
    return HttpResponse(template.render(context, request))


def courses_view(request):
    template = loader.get_template('manager/courses.html')
    course = Course.objects.all()
    about = AboutUs.objects.values().first()
    context = {
        "about": about,
        "course": course,
    }
    return HttpResponse(template.render(context, request))


def admin_courses_view(request):
    template = loader.get_template('secretary/courses.html')
    course = Course.objects.all()
    about = AboutUs.objects.values().first()
    context = {
        "about": about,
        "course": course,
    }
    return HttpResponse(template.render(context, request))


def user_courses_view(request, pk):
    template = loader.get_template('user/course.html')
    about = AboutUs.objects.values().first()
    participants = Participants.objects.filter(user=pk).all()

    context = {
        "about": about,
        "participants": participants,
    }
    return HttpResponse(template.render(context, request))


def teacher_courses_view(request, pk):
    template = loader.get_template('teacher/courses.html')
    about = AboutUs.objects.values().first()
    participants = Participants.objects.filter(user=pk).all()
    context = {
        "about": about,
        "participants": participants,
    }
    return HttpResponse(template.render(context, request))


def session_view(request):
    template = loader.get_template('manager/sessions.html')
    session = Sessions.objects.all()
    about = AboutUs.objects.values().first()
    context = {
        "about": about,
        "session": session,
    }
    return HttpResponse(template.render(context, request))


def admin_session_view(request):
    template = loader.get_template('secretary/sessions.html')
    session = Sessions.objects.all()
    about = AboutUs.objects.values().first()
    context = {
        "about": about,
        "session": session,
    }
    return HttpResponse(template.render(context, request))


def day_view(request):
    template = loader.get_template('manager/days.html')
    day = Days.objects.all()
    about = AboutUs.objects.values().first()
    context = {
        "about": about,
        "day": day,
    }
    return HttpResponse(template.render(context, request))


def admin_day_view(request):
    template = loader.get_template('secretary/days.html')
    day = Days.objects.all()
    about = AboutUs.objects.values().first()
    context = {
        "about": about,
        "day": day,
    }
    return HttpResponse(template.render(context, request))


class CourseView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class SearchView(viewsets.generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'title']

    def get_queryset(self):
        return Course.objects.filter(sport=self.kwargs['pk'])


class DaysView(viewsets.ModelViewSet):
    queryset = Days.objects.all()
    serializer_class = DaysSerializer

    def get_queryset(self):
        queryset = Days.objects.filter(session=self.kwargs.get('pk'))
        return queryset

    def destroy(self, request, *args, **kwargs):
        queryset = Days.objects.filter(id=self.kwargs.get('pk'))
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SessionView(viewsets.ModelViewSet):
    queryset = Sessions.objects.all()
    serializer_class = SessionSerializer

    def get_queryset(self):
        queryset = Sessions.objects.filter(course=self.kwargs.get('pk'))
        return queryset

    def destroy(self, request, *args, **kwargs):
        queryset = Sessions.objects.get(id=kwargs.get('pk'))
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ParticipationView(viewsets.ViewSet):
    queryset = Participants.objects.all()
    serializer_class = ParticipantsSerializer
    permission_classes = [IsAuthenticated]

    def list(self):
        queryset = Participants.objects.filter(user=self.request.user.id)
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
                session = Sessions.objects.filter(id=data["session"]).first()
                day = Days.objects.filter(id=data["day"]).first()
                course = Course.objects.filter(id=data["course"]).first()
                Participants.objects.update_or_create(title=data["title"],
                                                      description=data["description"],
                                                      session=session,
                                                      day=day,
                                                      price=data["price"],
                                                      user=self.request.user,
                                                      course=course,
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


class ManagerParticipationView(viewsets.ModelViewSet):
    queryset = Participants.objects.all()
    serializer_class = ParticipantsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        data = self.request.data
        session = Sessions.objects.filter(id=data["session"]).first()
        day = Days.objects.filter(id=data["day"]).first()
        course = Course.objects.filter(id=self.kwargs['id']).first()
        user = User.objects.filter(id=data["user"]).first()
        participants = Participants.objects.update_or_create(title=data["title"],
                                                             description=data["description"],
                                                             session=session,
                                                             day=day,
                                                             price=data["price"],
                                                             user=user,
                                                             course=course,
                                                             created=self.request.user)
        serializer = ParticipantsSerializer(participants)
        return Response(serializer.data)


class SportView(viewsets.ModelViewSet):
    queryset = Sport.objects.all()
    serializer_class = SportSerializer


class CourseUserView(generics.ListAPIView):
    queryset = Participants.objects.all()
    serializer_class = ParticipantsUserSerializer
    lookup_field = "id"


@api_view(('GET',))
def verify(request):
    participants = Participants.objects.get(authority=request.GET.get('Authority', ''))
    about = AboutUs.objects.values().first()
    sport = Sport.objects.all().values()

    context = {
        "about": about,
        "sport": sport,
        "participants": participants
    }

    authority_data = {
        "MerchantID": settings.MERCHANT,
        "Authority": participants.authority,
        "Amount": participants.price
    }

    data = json.dumps(authority_data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
    response = response.json()
    if response['Status'] == 100:
        template = loader.get_template('public/check.html')
        participants.success = True
        participants.save()
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('public/error.html')
        participants.delete()
        return HttpResponse(template.render(context, request))
