import requests
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.utils import json
from About.models import AboutUs
from Calendar.models import Day
from PowerGrow.decorators import session_auth_required
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


@cache_page(60 * 15)
def category_view(request, pk):
    about = AboutUs.objects.first()  # Assuming there's only one AboutUs instance
    sport = get_object_or_404(Sport, id=pk)  # Ensure the sport exists
    courses = Course.objects.filter(sport=sport, active=True)
    sports = Sport.objects.all()

    context = {
        "about": about,
        "sport": sport,
        "course": courses,
        "sports": sports  # اضافه کردن لیست ورزش‌ها به کانتکست
    }

    return render(request, 'public/category.html', context)


@cache_page(60 * 15)
def product_view(request, pk):
    about = AboutUs.objects.first()
    sport = Sport.objects.all()
    product = get_object_or_404(Course, id=pk)
    session = Session.objects.all().filter(course_id=pk).order_by("number")
    participants = Participants.objects.filter(
        course=product,
        user__is_teacher=False,
        user__is_superuser=False,
        user__is_staff=False,
        price__gt=0,
        success=True
    )

    context = {
        "about": about,
        "product": product,
        "participants": participants,
        "sport": sport,
        "session": session,
    }

    return render(request, 'public/product.html', context)


def get_days_for_session(request):
    session_id = request.GET.get('session_id')
    days = Days.objects.filter(session_id=session_id).values('id', 'title', 'tuition', 'off')
    return JsonResponse(list(days), safe=False)


@session_auth_required
def payment_view(request, pk, session, day, start):
    about = AboutUs.objects.first()  # Assuming there's only one AboutUs instance
    product = get_object_or_404(Course, id=pk)
    sessions = get_object_or_404(Session, id=session)
    days = get_object_or_404(Days, id=day)
    start_day = get_object_or_404(Day, id=start)

    context = {
        "about": about,
        "product": product,
        "session": sessions,
        "day": days,
        "start": start_day,
    }

    return render(request, 'public/payment.html', context)


@api_view(['GET'])
def verify(request):
    authority = request.GET.get('Authority', '')
    participants = get_object_or_404(Participants, authority=authority)

    about = AboutUs.objects.first()  # Assuming there's only one AboutUs instance
    sport = Sport.objects.all()

    authority_data = {
        "MerchantID": settings.MERCHANT,
        "Authority": participants.authority,
        "Amount": participants.price
    }

    data = json.dumps(authority_data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
    response_data = response.json()

    if response_data.get('Status') == 100:
        participants.success = True
        participants.save()
        return render(request, 'public/check.html', {
            "about": about,
            "sport": sport,
            "participants": participants
        })
    else:
        participants.delete()
        return render(request, 'public/error.html', {
            "about": about,
            "sport": sport,
            "participants": participants
        })


@cache_page(60 * 15)
def manager_sports_view(request):
    sport = Sport.objects.all()
    about = AboutUs.objects.values().first()
    context = {
        "about": about,
        "sport": sport,
    }
    return render(request, 'manager/sports.html', context)


def admin_sports_view(request):
    sport = Sport.objects.all()
    about = AboutUs.objects.first()
    context = {
        "about": about,
        "sport": sport,
    }
    return render(request, 'admin/sports.html', context)


def manager_courses_view(request):
    # بارگذاری اطلاعات دوره‌ها و اطلاعات اضافی
    courses = Course.objects.all().order_by("-pk")
    about = AboutUs.objects.first()
    users = User.objects.all()

    # پیاده‌سازی pagination
    paginator = Paginator(courses, 50)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)  # اگر شماره صفحه معتبر نبود، به صفحه اول برگردیم

    # آماده‌سازی context برای الگو
    context = {
        "about": about,
        "page_obj": page_obj,
        "users": users
    }

    # استفاده از render برای بارگذاری الگو
    return render(request, 'manager/courses.html', context)


def admin_courses_view(request):
    courses = Course.objects.all().order_by("-pk")
    about = AboutUs.objects.first()
    users = User.objects.all()

    # پیاده‌سازی pagination
    paginator = Paginator(courses, 50)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)  # اگر شماره صفحه معتبر نبود، به صفحه اول برگردیم

    # آماده‌سازی context برای الگو
    context = {
        "about": about,
        "page_obj": page_obj,
        "users": users
    }

    # استفاده از render برای بارگذاری الگو
    return render(request, 'admin/courses.html', context)


def teacher_courses_view(request, pk):
    # بارگذاری اطلاعات مربوط به AboutUs
    about = AboutUs.objects.first()

    # بارگذاری شرکت‌کنندگان مربوط به معلم
    participants = Participants.objects.filter(user=pk)

    # آماده‌سازی context برای الگو
    context = {
        "about": about,
        "participants": participants,
        "user": pk,
    }

    # استفاده از render برای بارگذاری الگو
    return render(request, 'teacher/courses.html', context)


def user_courses_view(request, pk):
    # بارگذاری اطلاعات مربوط به AboutUs
    about = AboutUs.objects.first()

    # بارگذاری شرکت‌کنندگان مربوط به کاربر
    participants = Participants.objects.filter(user_id=pk, success=True)

    # آماده‌سازی context برای الگو
    context = {
        "about": about,
        "participants": participants,
    }

    # استفاده از render برای بارگذاری الگو
    return render(request, 'user/course.html', context)


def manager_session_view(request):
    # بارگذاری اطلاعات مربوط به AboutUs
    about = AboutUs.objects.first()

    # بارگذاری تمامی جلسات
    sessions = Session.objects.all()

    # پیاده‌سازی pagination
    paginator = Paginator(sessions, 50)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)  # اگر شماره صفحه معتبر نبود، به صفحه اول برگردیم

    # آماده‌سازی context برای الگو
    context = {
        "about": about,
        "page_obj": page_obj,
    }

    # استفاده از render برای بارگذاری الگو
    return render(request, 'manager/sessions.html', context)


def admin_session_view(request):
    # بارگذاری اطلاعات مربوط به AboutUs
    about = AboutUs.objects.first()

    # بارگذاری تمامی جلسات
    sessions = Session.objects.all()

    # آماده‌سازی context برای الگو
    context = {
        "about": about,
        "sessions": sessions,
    }

    # استفاده از render برای بارگذاری الگو
    return render(request, 'admin/sessions.html', context)


def manager_days_view(request):
    # بارگذاری اطلاعات مربوط به AboutUs
    about = AboutUs.objects.first()

    # بارگذاری تمامی روزها
    days = Days.objects.all()

    # پیاده‌سازی pagination
    paginator = Paginator(days, 50)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)  # اگر شماره صفحه معتبر نبود، به صفحه اول برگردیم

    # آماده‌سازی context برای الگو
    context = {
        "about": about,
        "page_obj": page_obj,
    }

    # استفاده از render برای بارگذاری الگو
    return render(request, 'manager/days.html', context)


def admin_days_view(request):
    # بارگذاری اطلاعات مربوط به AboutUs
    about = AboutUs.objects.first()

    # بارگذاری تمامی روزها
    days = Days.objects.all()

    # آماده‌سازی context برای الگو
    context = {
        "about": about,
        "days": days,  # تغییر نام به 'days' برای وضوح بیشتر
    }

    # استفاده از render برای بارگذاری الگو
    return render(request, 'admin/days.html', context)


def manager_user_list(request, pk):
    # بارگذاری اطلاعات مربوط به AboutUs
    about = AboutUs.objects.first()

    # بارگذاری دوره با استفاده از get_object_or_404
    participants = get_object_or_404(Participants, course=pk)

    paginator = Paginator(participants, 100)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)  # اگر شماره صفحه معتبر نبود، به صفحه اول برگردیم

    # محاسبه تعداد شرکت‌کنندگان
    participant_count = course.participants.count()

    # آماده‌سازی context برای الگو
    context = {
        "about": about,
        "page_obj": page_obj,
        "size": participant_count,
    }

    # استفاده از render برای بارگذاری الگو
    return render(request, 'manager/list.html', context)


def teacher_user_list(request, pk, id):
    # بارگذاری اطلاعات مربوط به AboutUs
    about = AboutUs.objects.first()

    # بارگذاری دوره و کاربر با استفاده از get_object_or_404
    course = get_object_or_404(Course, id=pk)
    user = get_object_or_404(User, id=id)

    # محاسبه تعداد شرکت‌کنندگان
    participant_count = course.participants.count()

    # آماده‌سازی context برای الگو
    context = {
        "about": about,
        "course": course,
        "user": user,
        "size": participant_count,
    }

    # استفاده از render برای بارگذاری الگو
    return render(request, 'teacher/users.html', context)


class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminUser]


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        course_id = self.kwargs.get('pk')
        return super().get_queryset().filter(pk=course_id)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SportListCreateView(generics.ListCreateAPIView):
    queryset = Sport.objects.all()
    serializer_class = SportSerializer
    permission_classes = [IsAdminUser]


class SportDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sport.objects.all()
    serializer_class = SportSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        sport_id = self.kwargs.get('pk')
        return super().get_queryset().filter(pk=sport_id)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DaysListCreateView(generics.ListCreateAPIView):
    queryset = Days.objects.all()
    serializer_class = DaysSerializer
    permission_classes = [IsAdminUser]


class DaysDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Days.objects.all()
    serializer_class = DaysSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        session_id = self.kwargs.get('pk')
        return super().get_queryset().filter(pk=session_id)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SessionListCreateView(generics.ListCreateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsAdminUser]


class SessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        course_id = self.kwargs.get('pk')  # فرض بر این است که شما ID دوره را از URL دریافت می‌کنید
        return super().get_queryset().filter(course=course_id)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ParticipationCreateView(viewsets.ViewSet):
    queryset = Participants.objects.all()
    serializer_class = ParticipantsSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        data = request.data
        # Validate required fields
        required_fields = ['price', 'session', 'day', 'startDay', 'course']
        for field in required_fields:
            if field not in data:
                return Response({'error': f'Missing field: {field}'}, status=status.HTTP_400_BAD_REQUEST)

        authority_data = {
            "MerchantID": settings.MERCHANT,
            "Amount": data["price"],
            "phone": str(request.user.number),
            "Description": data["description"],
            "CallbackURL": CallbackURL,
        }

        try:
            response = requests.post(ZP_API_REQUEST, json=authority_data, timeout=10)
            response_data = response.json()

            if response_data.get('Status') == 100:
                session = Session.objects.filter(id=data["session"]).first()
                week = Days.objects.filter(id=data["day"]).first()
                start = Day.objects.filter(id=data["startDay"]).first()
                course = Course.objects.get(id=data["course"])

                day = week.title.split("،")
                ids = Day.objects.filter(name__in=day, month__number__gte=start.month.number,
                                         month__year__number__gte=start.month.year.number, holiday=False).exclude(
                    month__number=start.month.number,
                    number__lt=start.number) \
                          .order_by('pk').values_list('pk', flat=True)[:int(session.number)]
                end = Day.objects.filter(pk__in=list(ids)).last()

                participant_data = {
                    'description': data["description"],
                    'startDay': start.id,
                    'endDay': end.id,
                    'session': session.id,
                    'day': week.id,
                    'price': data["price"],
                    'user': request.user.id,
                    'course': course.id,
                    'authority': str(response_data['Authority']),
                    'success': False
                }

                serializer = self.serializer_class(data=participant_data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response({'payment': ZP_API_STARTPAY, 'authority': str(response_data['Authority'])},
                                    status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'Validation failed', 'details': serializer.errors},
                                    status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'error': 'Payment request failed'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': 'An unexpected error occurred', 'details': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ManagerParticipationView(viewsets.ViewSet):
    serializer_class = ManagerParticipantsSerializer
    permission_classes = [IsAdminUser]

    def create(self, request):
        data = request.data
        # Validate required fields
        required_fields = ['price', 'session', 'day', 'startDay', 'course']
        for field in required_fields:
            if field not in data:
                return Response({'error': f'Missing field: {field}'}, status=status.HTTP_400_BAD_REQUEST)

        course = Course.objects.filter(id=self.kwargs['id']).first()
        user = User.objects.filter(number=self.kwargs['user']).first()
        start = Day.objects.filter(id=self.kwargs['start']).first()
        week = Days.objects.filter(id=self.kwargs['day']).first()
        session = Session.objects.filter(id=self.kwargs['session']).first()

        day = week.title.split("،")

        startIds = Day.objects.filter(name__in=day, month__number__gte=start.month.number,
                                 month__year__number__gte=start.month.year.number, holiday=False).exclude(
            month__number=start.month.number,
            number__lt=start.number) \
                  .order_by('pk').values_list('pk', flat=True)[:int(session.number)]
        startDay = Day.objects.filter(pk__in=list(startIds)).first()

        endIds = Day.objects.filter(name__in=day, month__number__gte=start.month.number,
                                 month__year__number__gte=start.month.year.number, holiday=False).exclude(
            month__number=start.month.number,
            number__lt=start.number) \
                  .order_by('pk').values_list('pk', flat=True)[:int(session.number)]
        endDay = Day.objects.filter(pk__in=list(endIds)).last()

        participant_data = {
            'description': data["description"],
            'startDay': startDay.id,
            'endDay': endDay.id,
            'session': session.id,
            'day': week.id,
            'price': data["price"],
            'user': user,
            'course': course.id,
            'success': True,
            'created': request.user.id
        }

        serializer = self.serializer_class(data=participant_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Validation failed', 'details': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        try:
            participant = Participants.objects.get(pk=pk)
        except Participants.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(participant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        try:
            participant = Participants.objects.get(pk=pk)
            participant.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Participants.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
