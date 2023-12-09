from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from About.models import AboutUs
from Product.models import Participants, Sport
from Reservation.models import Reservations
from User.serializer import *
from User.models import *


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
def register_view(request):
    about = AboutUs.objects.values().first()
    template = loader.get_template('public/register.html')
    context = {
        "about": about,
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


def user_home_view(request, pk):
    about = AboutUs.objects.values().first()
    template = loader.get_template('user/dashboard.html')
    user = User.objects.all().get(id=pk)
    context = {
        "about": about,
        "user": user,
    }
    return HttpResponse(template.render(context, request))


def user_gym_view(request, pk):
    about = AboutUs.objects.values().first()
    template = loader.get_template('user/gym.html')
    reservation = Reservations.objects.filter(id=pk)
    context = {
        "about": about,
        "reservation" : reservation

    }
    return HttpResponse(template.render(context, request))


def user_course_view(request, pk):
    about = AboutUs.objects.values().first()
    template = loader.get_template('user/product.html')
    participants = Participants.objects.get(id=pk)
    size = Participants.objects.filter(course__pk=participants.course.id).values()
    context = {
        "about": about,
        "participants" : participants,
        "size" : len(list(size))

    }
    return HttpResponse(template.render(context, request))


def teacher_home_view(request, pk):
    about = AboutUs.objects.values().first()
    template = loader.get_template('teacher/dashboard.html')
    user = User.objects.all().get(id=pk)
    context = {
        "about": about,
        "id": pk,
        "user" : user
    }
    return HttpResponse(template.render(context, request))


def secretary_home_view(request, pk):
    about = AboutUs.objects.values().first()
    template = loader.get_template('secretary/dashboard.html')
    user = User.objects.all().get(id=pk)
    context = {
        "about": about,
        "user" : user

    }
    return HttpResponse(template.render(context, request))


def manager_home_view(request, pk):
    about = AboutUs.objects.values().first()
    template = loader.get_template('manager/dashboard.html')
    user = User.objects.all().get(id=pk)
    context = {
        "about": about,
        "user" : user
    }
    return HttpResponse(template.render(context, request))


def profile_view(request, pk):
    about = AboutUs.objects.values().first()
    template = loader.get_template('public/profile.html')
    user = User.objects.filter(id=pk).values().first()
    context = {
        "about": about,
        "user" : user
    }
    return HttpResponse(template.render(context, request))


def user_view(request):
    about = AboutUs.objects.values().first()
    template = loader.get_template('manager/users.html')
    user = User.objects.all()
    context = {
        "about": about,
        "user" : user
    }
    return HttpResponse(template.render(context, request))


def admin_user_view(request):
    about = AboutUs.objects.values().first()
    template = loader.get_template('secretary/users.html')
    user = User.objects.all()
    context = {
        "about": about,
        "user" : user
    }
    return HttpResponse(template.render(context, request))



class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = User.objects.get(id=token.user_id)
        return Response({'token': token.key, 'user': GetAccountSerializer(user).data})


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UpdateProfile(generics.UpdateAPIView, ):
    queryset = User.objects.all()
    lookup_field = "number"
    serializer_class = UpdateProfileSerializer


@permission_classes([IsAuthenticated])
class AdminRegisterUser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminRegisterSerializer


@permission_classes([IsAuthenticated])
class SecretaryRegisterUser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SecretaryRegisterSerializer


class ChangePasswordView(generics.UpdateAPIView, ):
    queryset = User.objects.all()
    lookup_field = "number"
    permission_classes = (AllowAny,)
    serializer_class = ChangePasswordSerializer


class ChangeSalaryView(generics.UpdateAPIView, ):
    queryset = User.objects.all()
    lookup_field = "number"
    permission_classes = (AllowAny,)
    serializer_class = ChangeSalarySerializer


class ChangeDebtView(generics.UpdateAPIView, ):
    queryset = User.objects.all()
    lookup_field = "number"
    permission_classes = (AllowAny,)
    serializer_class = ChangeDebtSerializer


class DeleteAccount(generics.UpdateAPIView, ):
    queryset = User.objects.all()
    lookup_field = "id"
    permission_classes = (AllowAny,)
    serializer_class = DeleteAccountSerializer


@permission_classes([AllowAny])
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


@permission_classes([AllowAny])
class GetAccount(generics.ListAPIView, ):
    queryset = User.objects.all()
    lookup_field = "number"
    serializer_class = GetAccountSerializer

    def get_queryset(self):
        queryset = User.objects.filter(number=self.kwargs.get('number'))
        return queryset


class GetAllAccount(generics.ListCreateAPIView, ):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = GetAccountSerializer


class ManagePermission(generics.UpdateAPIView, ):
    queryset = User.objects.all()
    lookup_field = "number"
    serializer_class = ManagePermissionSerializer


class ManageAccess(generics.UpdateAPIView, ):
    queryset = User.objects.all()
    lookup_field = "number"
    serializer_class = ManageAccessSerializer

