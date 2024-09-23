from django.http import HttpResponse
from django.template import loader
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets, filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from About.models import AboutUs
from Product.models import *
from Reservation.models import Reservations
from User.serializer import *
from User.models import *


@cache_page(60 * 15)
def login_view(request):
    about = AboutUs.objects.values().first()
    template = loader.get_template('public/login.html')
    sport = Sport.objects.all().values()

    context = {
        "about": about,
        "sport": sport,

    }
    return HttpResponse(template.render(context, request))


@csrf_exempt
@cache_page(60 * 15)
def register_view(request):
    about = AboutUs.objects.values().first()
    template = loader.get_template('public/register.html')
    sport = Sport.objects.all().values()
    context = {
        "about": about,
        "sport": sport,

    }
    return HttpResponse(template.render(context, request))


def verification_view(request, number):
    about = AboutUs.objects.values().first()
    data = {'to': number}
    response = requests.post('https://console.melipayamak.com/api/send/otp/d15bf0639e874ecebb5040b599cb8af6', json=data)
    template = loader.get_template('public/verification.html')
    context = {
        "number": number,
        "about": about,
        "response": response.json()
    }
    return HttpResponse(template.render(context, request))


def forget_view(request):
    about = AboutUs.objects.values().first()
    template = loader.get_template('public/forget.html')
    context = {
        "about": about,
    }
    return HttpResponse(template.render(context, request))


def pass_view(request, number):
    about = AboutUs.objects.values().first()
    template = loader.get_template('public/password.html')
    context = {
        "number": number,
        "about": about,

    }
    return HttpResponse(template.render(context, request))


@cache_page(60 * 15)
def user_home_view(request, pk):
    about = AboutUs.objects.values().first()
    template = loader.get_template('user/dashboard.html')
    user = User.objects.all().get(id=pk)
    context = {
        "about": about,
        "user": user,
    }
    return HttpResponse(template.render(context, request))


@cache_page(60 * 15)
def user_gym_view(request, pk):
    about = AboutUs.objects.values().first()
    template = loader.get_template('user/gym.html')
    reservation = Reservations.objects.get(id=pk)
    sport = Sport.objects.all().values()
    context = {
        "about": about,
        "reservation": reservation,
        "sport": sport,
    }
    return HttpResponse(template.render(context, request))


@cache_page(60 * 15)
def user_product_view(request, pk):
    about = AboutUs.objects.values().first()
    template = loader.get_template('user/product.html')
    participants = Participants.objects.get(id=pk)
    sport = Sport.objects.all().values()
    size = Participants.objects.filter(course__pk=participants.course.id).values()
    context = {
        "about": about,
        "participants": participants,
        "size": len(list(size)),
        "sport": sport,

    }
    return HttpResponse(template.render(context, request))


@cache_page(60 * 15)
def teacher_home_view(request, pk):
    about = AboutUs.objects.values().first()
    template = loader.get_template('teacher/dashboard.html')
    user = User.objects.all().get(id=pk)
    context = {
        "about": about,
        "id": pk,
        "user": user
    }
    return HttpResponse(template.render(context, request))


@cache_page(60 * 15)
def secretary_home_view(request, pk):
    about = AboutUs.objects.values().first()
    template = loader.get_template('secretary/dashboard.html')
    user = User.objects.all().get(id=pk)
    context = {
        "about": about,
        "user": user

    }
    return HttpResponse(template.render(context, request))


@cache_page(60 * 15)
def manager_home_view(request, pk):
    about = AboutUs.objects.values().first()
    template = loader.get_template('manager/dashboard.html')
    user = User.objects.all().get(id=pk)
    context = {
        "about": about,
        "user": user
    }
    return HttpResponse(template.render(context, request))


def profile_view(request, pk):
    about = AboutUs.objects.values().first()
    template = loader.get_template('public/profile.html')
    user = User.objects.filter(id=pk).values().first()
    context = {
        "about": about,
        "user": user
    }
    return HttpResponse(template.render(context, request))


def salary_view(request, pk):
    about = AboutUs.objects.values().first()
    template = loader.get_template('teacher/salary.html')
    user = User.objects.get(id=pk)
    ids = User.objects.filter(id=pk).values_list("participants__course__id", flat=True)
    size = User.objects.filter(id=pk).values_list("participants__course", flat=True)
    participants = Participants.objects.filter(course_id__in=ids, user__is_teacher=False,
                                               user__is_superuser=False, user__is_staff=False,
                                               price__gt=0, success=True)

    course = Course.objects.filter(participants__user__id=pk)

    context = {
        "about": about,
        "user": user,
        "course": course,
        "participants": len(list(participants)),
        "active": participants,
        "size": len(list(size)),

    }
    return HttpResponse(template.render(context, request))


def user_view(request):
    about = AboutUs.objects.values().first()
    template = loader.get_template('manager/users.html')
    user = User.objects.all()
    p = Paginator(user, 50)
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
        'page_obj': page_obj
    }
    return HttpResponse(template.render(context, request))


def admin_user_view(request):
    template = loader.get_template('secretary/users.html')
    about = AboutUs.objects.values().first()
    user = User.objects.all()
    p = Paginator(user, 50)
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
        'page_obj': page_obj
    }
    return HttpResponse(template.render(context, request))


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # احراز هویت کاربر
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        # ایجاد پاسخ و تنظیم کوکی
        response = Response({
            'message': 'Login successful',
            'user_id': user.pk,
            'username': user.username
        })

        # تنظیم کوکی با ویژگی‌های HttpOnly و Secure
        response.set_cookie(
            key='token',
            value=token.key,
            httponly=True,  # فقط از طریق HTTP قابل دسترسی است
            secure=True,  # فقط از طریق HTTPS ارسال می‌شود
            samesite='Lax'  # جلوگیری از ارسال کوکی در درخواست‌های بین‌سایتی
        )

        return response


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@permission_classes([IsAdminUser])
class UpdateProfile(generics.UpdateAPIView, ):
    queryset = User.objects.all()
    lookup_field = "number"
    serializer_class = UpdateProfileSerializer


@permission_classes([IsAdminUser])
class AdminRegisterUser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminRegisterSerializer


@permission_classes([IsAdminUser])
class SecretaryRegisterUser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SecretaryRegisterSerializer


class ChangePasswordView(generics.UpdateAPIView, ):
    queryset = User.objects.all()
    lookup_field = "number"
    permission_classes = (AllowAny,)
    serializer_class = ChangePasswordSerializer


@permission_classes([IsAdminUser])
class ChangeSalaryView(generics.UpdateAPIView, ):
    queryset = User.objects.all()
    lookup_field = "pk"
    permission_classes = (AllowAny,)
    serializer_class = ChangeSalarySerializer


@permission_classes([IsAdminUser])
class ChangeDebtView(generics.UpdateAPIView, ):
    queryset = User.objects.all()
    lookup_field = "pk"
    permission_classes = (AllowAny,)
    serializer_class = ChangeDebtSerializer


@permission_classes([IsAdminUser])
class DeleteAccount(generics.UpdateAPIView, ):
    queryset = User.objects.all()
    lookup_field = "id"
    permission_classes = (AllowAny,)
    serializer_class = DeleteAccountSerializer


class ActivateAccount(generics.UpdateAPIView, ):
    queryset = User.objects.all()
    lookup_field = "number"
    serializer_class = DeleteAccountSerializer


@api_view(['GET'])
def get_user(request, number):
    user = User.objects.filter(number=number)
    ser = GetAccountSerializer(user, many=True)
    if not user:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(ser.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_verification(request, number):
    user = User.objects.filter(number=number).values().first()
    if user["is_active"]:
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@permission_classes([IsAdminUser])
class GetAccount(generics.ListAPIView, ):
    queryset = User.objects.all()
    lookup_field = "number"
    serializer_class = GetAccountSerializer

    def get_queryset(self):
        queryset = User.objects.filter(number=self.kwargs.get('number'))
        return queryset


@permission_classes([IsAdminUser])
class GetAllAccount(generics.ListCreateAPIView, ):
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name", "number"]
    serializer_class = GetAccountSerializer


@permission_classes([IsAdminUser])
class ManagePermission(generics.UpdateAPIView, ):
    queryset = User.objects.all()
    lookup_field = "number"
    serializer_class = ManagePermissionSerializer


@permission_classes([IsAdminUser])
class ManageAccess(generics.UpdateAPIView, ):
    queryset = User.objects.all()
    lookup_field = "number"
    serializer_class = ManageAccessSerializer


@permission_classes([IsAdminUser])
class ChangeNameView(generics.UpdateAPIView, ):
    queryset = User.objects.all()
    lookup_field = "pk"
    serializer_class = ChangeNameSerializer


@permission_classes([IsAdminUser])
class ChangeNumberView(generics.UpdateAPIView, ):
    queryset = User.objects.all()
    lookup_field = "pk"
    serializer_class = ChangeNumberSerializer


@permission_classes([IsAdminUser])
class ChangeBirthView(generics.UpdateAPIView, ):
    queryset = User.objects.all()
    lookup_field = "pk"
    serializer_class = ChangeBirthSerializer


@permission_classes([IsAdminUser])
class ChangePassView(generics.UpdateAPIView, ):
    queryset = User.objects.all()
    lookup_field = "pk"
    serializer_class = ChangePasswordSerializer


@permission_classes([IsAdminUser])
class ChangeDescriptionView(generics.UpdateAPIView, ):
    queryset = User.objects.all()
    lookup_field = "pk"
    serializer_class = ChangeDescriptionSerializer
