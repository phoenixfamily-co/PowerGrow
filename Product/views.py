import requests
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, filters, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.utils import json
from About.models import AboutUs
from Calendar.models import Day
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


def product_view(request, pk):
    about = AboutUs.objects.values().first()
    sport = Sport.objects.all().values()
    product = Course.objects.get(id=pk)
    participants = Participants.objects.filter(course__pk=pk, user__is_teacher=False,
                                               user__is_superuser=False, user__is_staff=False,
                                               price__gt=0, success=True)

    template = loader.get_template('public/product.html')
    context = {
        "about": about,
        "product": product,
        "participants": participants,
        "sport": sport,

    }
    return HttpResponse(template.render(context, request))


def payment_view(request, pk, session, day, start):
    about = AboutUs.objects.values().first()
    product = Course.objects.filter(id=pk).values().first()
    sessions = Sessions.objects.filter(id=session).values().first()
    days = Days.objects.filter(id=day).values().first()
    day = Day.objects.get(id=start)
    template = loader.get_template('public/payment.html')
    context = {
        "about": about,
        "product": product,
        "session": sessions,
        "day": days,
        "start": day,
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


@cache_page(60 * 15)
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


@cache_page(60 * 15)
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
    user = User.objects.all()
    p = Paginator(course, 50)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)

    context = {
        "about": about,
        'page_obj': page_obj,
        "user": user
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
        "user": pk,
    }
    return HttpResponse(template.render(context, request))


def session_view(request):
    template = loader.get_template('manager/sessions.html')
    session = Sessions.objects.all()
    about = AboutUs.objects.values().first()

    p = Paginator(session, 50)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)

    context = {
        "about": about,
        'page_obj': page_obj,
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

    p = Paginator(day, 50)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    context = {
        "about": about,
        'page_obj': page_obj,
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


def teacher_user_list(request, pk, user):
    about = AboutUs.objects.values().first()
    template = loader.get_template('teacher/users.html')
    course = Course.objects.get(id=pk)
    user = User.objects.get(id=user)
    size = course.participants.values()
    context = {
        "about": about,
        "course": course,
        "user": user,
        "size": len(list(size)),

    }
    return HttpResponse(template.render(context, request))


def manager_user_list(request, pk):
    about = AboutUs.objects.values().first()
    template = loader.get_template('manager/list.html')
    course = Course.objects.get(id=pk)
    size = course.participants.values()
    context = {
        "about": about,
        "course": course,
        "size": len(list(size)),

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

    def update(self, request, *args, **kwargs):
        Days.objects.filter(id=kwargs.get('pk')).update(title=self.request.data['title'],
                                                        tuition=self.request.data['tuition'],
                                                        off=self.request.data['off'],
                                                        end=self.request.data['end'],
                                                        session=self.request.data['session'])
        return Response(status=status.HTTP_202_ACCEPTED)


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

    def update(self, request, *args, **kwargs):
        Sessions.objects.filter(id=kwargs.get('pk')).update(number=self.request.data['number'])
        return Response(status=status.HTTP_202_ACCEPTED)


# This class uses ZP_API_REQUEST, STARTPAY, calback

class ParticipationView(viewsets.ViewSet):
    queryset = Participants.objects.all()
    serializer_class = ParticipantsSerializer
    permission_classes = [IsAuthenticated]

    def list(self):
        queryset = Participants.objects.filter(user=self.request.user.id)
        return queryset

    def create(self, request):
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
                week = Days.objects.filter(id=data["day"]).first()
                start = Day.objects.filter(id=data["start"]).first()
                course = Course.objects.filter(id=data["course"]).first()
                day = week.title.split("،")
                ids = Day.objects.filter(name__in=day, month__number__gte=start.month.number,
                                         month__year__number__gte=start.month.year.number, holiday=False).exclude(
                    month__number=start.month.number,
                    number__lt=start.number).order_by('pk').values_list('pk', flat=True)[:int(session.number)]
                end = Day.objects.filter(pk__in=list(ids)).last()
                Participants.objects.update_or_create(title=data["title"],
                                                      description=data["description"],
                                                      startDay=start,
                                                      endDay=end,
                                                      session=session,
                                                      day=week,
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


@api_view(('POST',))
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


class ManagerParticipationView(viewsets.ModelViewSet):
    queryset = Participants.objects.all()
    serializer_class = ManagerParticipantsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        data = self.request.data
        course = Course.objects.filter(id=self.kwargs['id']).first()
        user = User.objects.filter(number=self.kwargs['user']).first()
        start = Day.objects.filter(id=self.kwargs['start']).first()
        week = Days.objects.filter(id=self.kwargs['day']).first()
        session = Sessions.objects.filter(id=self.kwargs['session']).first()
        day = week.title.split("،")
        ids = Day.objects.filter(name__in=day, month__number__gte=start.month.number,
                                 month__year__number__gte=start.month.year.number, holiday=False).exclude(
            month__number=start.month.number,
            number__lt=start.number) \
                  .order_by('pk').values_list('pk', flat=True)[:int(session.number)]
        end = Day.objects.filter(pk__in=list(ids)).last()

        participants = Participants.objects.update_or_create(title=data["title"],
                                                             description=data["description"],
                                                             session=session,
                                                             day=week,
                                                             endDay=end,
                                                             startDay=start,
                                                             price=data["price"],
                                                             user=user,
                                                             course=course,
                                                             success=True,
                                                             created=self.request.user)
        serializer = ParticipantsSerializer(participants)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        session = Sessions.objects.get(id=kwargs.get('session'))
        days = Days.objects.get(id=kwargs.get('day'))
        start = Day.objects.get(id=kwargs.get('start'))
        day = days.title.split("،")
        ids = Day.objects.filter(name__in=day, month__number__gte=start.month.number,
                                 month__year__number__gte=start.month.year.number, holiday=False).exclude(
            month__number=start.month.number,
            number__lt=start.number) \
                  .order_by('pk').values_list('pk', flat=True)[:int(session.number)]
        end = Day.objects.filter(pk__in=list(ids)).last()

        Participants.objects.filter(id=kwargs.get('id')).update(session=session,
                                                                day=days,
                                                                startDay=start,
                                                                endDay=end)
        return Response(status=status.HTTP_202_ACCEPTED)


@permission_classes([IsAdminUser])
class ChangeDayView(generics.UpdateAPIView, ):
    queryset = Participants.objects.all()
    lookup_field = "pk"
    serializer_class = ChangeDaySerializer


@permission_classes([IsAdminUser])
class ChangeDescriptionView(generics.UpdateAPIView, ):
    queryset = Participants.objects.all()
    lookup_field = "pk"
    serializer_class = ChangeDescriptionSerializer


@permission_classes([IsAdminUser])
class SportView(viewsets.ModelViewSet):
    queryset = Sport.objects.all()
    serializer_class = SportSerializer


# This class use zp_api_request

class CourseUserView(generics.ListAPIView):
    queryset = Participants.objects.all()
    serializer_class = ParticipantsUserSerializer
    lookup_field = "id"


@permission_classes([IsAdminUser])
class ChangeCourseTitle(generics.UpdateAPIView, ):
    queryset = Course.objects.all()
    lookup_field = "pk"
    serializer_class = ChangeTitleSerializer


@permission_classes([IsAdminUser])
class ChangeCourseName(generics.UpdateAPIView, ):
    queryset = Course.objects.all()
    lookup_field = "pk"
    serializer_class = ChangeNameSerializer


@permission_classes([IsAdminUser])
class ChangeCourseGender(generics.UpdateAPIView, ):
    queryset = Course.objects.all()
    lookup_field = "pk"
    serializer_class = ChangeGenderSerializer


@permission_classes([IsAdminUser])
class ChangeCourseType(generics.UpdateAPIView, ):
    queryset = Course.objects.all()
    lookup_field = "pk"
    serializer_class = ChangeTypeSerializer


@permission_classes([IsAdminUser])
class ChangeCourseTime(generics.UpdateAPIView, ):
    queryset = Course.objects.all()
    lookup_field = "pk"
    serializer_class = ChangeTimeSerializer


@permission_classes([IsAdminUser])
class ChangeCourseCapacity(generics.UpdateAPIView, ):
    queryset = Course.objects.all()
    lookup_field = "pk"
    serializer_class = ChangeCapacitySerializer


@permission_classes([IsAdminUser])
class ChangeCourseSport(generics.UpdateAPIView, ):
    queryset = Course.objects.all()
    lookup_field = "pk"
    serializer_class = ChangeSportSerializer


@permission_classes([IsAdminUser])
class UpdateCourse(generics.UpdateAPIView, ):
    queryset = Course.objects.all()
    lookup_field = "pk"
    serializer_class = UpdateCourseSerializer


@permission_classes([IsAdminUser])
class ChangeParticipantsPrice(generics.UpdateAPIView, ):
    queryset = Participants.objects.all()
    lookup_field = "pk"
    serializer_class = ChangePriceSerializer


@permission_classes([IsAdminUser])
class ChangeParticipantsDescription(generics.UpdateAPIView, ):
    queryset = Participants.objects.all()
    lookup_field = "pk"
    serializer_class = ChangeDescriptionSerializer


@permission_classes([IsAdminUser])
class ChangeParticipantsCourse(generics.UpdateAPIView, ):
    queryset = Participants.objects.all()
    lookup_field = "pk"
    serializer_class = ChangeCourseSerializer


@permission_classes([IsAdminUser])
class ChangeSessionCourse(generics.UpdateAPIView, ):
    queryset = Sessions.objects.all()
    lookup_field = "pk"
    serializer_class = UpdateSessionSerializer


@permission_classes([IsAdminUser])
class ChangeDaysCourse(generics.UpdateAPIView, ):
    queryset = Days.objects.all()
    lookup_field = "pk"
    serializer_class = UpdateDaysSerializer
