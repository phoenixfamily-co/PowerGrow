from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from About.models import AboutUs
from User.models import User
from User.serializer import RegisterSerializer, ChangePasswordSerializer, UpdateProfileSerializer, \
    DeleteAccountSerializer, GetAccountSerializer, ManagePermissionSerializer


def login_view(request):
    about = AboutUs.objects.values().first()
    template = loader.get_template('public/login.html')
    context = {
        "logo": about["logo"],
    }
    return HttpResponse(template.render(context, request))


@csrf_exempt
def register_view(request):
    about = AboutUs.objects.values().first()
    template = loader.get_template('public/register.html')
    context = {
        "logo": about["logo"],
    }
    return HttpResponse(template.render(context, request))


def verification_view(request, number):
    about = AboutUs.objects.values().first()
    template = loader.get_template('public/verification.html')
    context = {
        "number": number,
        "logo": about["logo"],

    }
    return HttpResponse(template.render(context, request))


def forget_view(request):
    about = AboutUs.objects.values().first()
    template = loader.get_template('public/forget.html')
    context = {
        "logo": about["logo"],
    }
    return HttpResponse(template.render(context, request))


def pass_view(request, number):
    about = AboutUs.objects.values().first()
    template = loader.get_template('public/password.html')
    context = {
        "number": number,
        "logo": about["logo"],

    }
    return HttpResponse(template.render(context, request))


def home_view(request):
    about = AboutUs.objects.values().first()
    template = loader.get_template('public/home.html')
    context = {
        "logo": about["logo"],
    }
    return HttpResponse(template.render(context, request))


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UpdateProfile(generics.UpdateAPIView, ):
    queryset = User.objects.all()
    lookup_field = "number"
    permission_classes = (AllowAny,)
    serializer_class = UpdateProfileSerializer


class ChangePasswordView(generics.UpdateAPIView, ):
    queryset = User.objects.all()
    lookup_field = "number"
    permission_classes = (AllowAny,)
    serializer_class = ChangePasswordSerializer


class DeleteAccount(generics.UpdateAPIView, ):
    queryset = User.objects.all()
    lookup_field = "number"
    permission_classes = (AllowAny,)
    serializer_class = DeleteAccountSerializer


class ActivateAccount(generics.UpdateAPIView, ):
    queryset = User.objects.all()
    lookup_field = "number"
    permission_classes = (AllowAny,)
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
def get_verification(request, number, code):
    user = User.objects.filter(number=number).values().first()
    if user["is_active"]:
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class GetAccount(generics.ListAPIView, ):
    queryset = User.objects.all()
    lookup_field = "number"
    permission_classes = (AllowAny,)
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
    permission_classes = (AllowAny,)
    serializer_class = ManagePermissionSerializer
