from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from User.models import User
from User.serializer import RegisterSerializer, ChangePasswordSerializer, UpdateProfileSerializer, \
    DeleteAccountSerializer, GetAccountSerializer, ManagePermissionSerializer


@csrf_exempt
def login_view(request):
    return render(request, "public/login.html")


@csrf_exempt
def register_view(request):
    return render(request, "public/register.html")


def verification_view(request):
    return render(request, "public/verification.html")


def forget_view(request):
    return render(request, "public/forget.html")


def pass_view(request, number):
    template = loader.get_template('public/password.html')
    context = {
        "number" : number
    }
    return HttpResponse(template.render(context, request))


def home_view(request):
    return render(request, "user/home.html")


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


@api_view(['GET'])
def get_selected(request, number):
    user = User.objects.filter(number=number)
    ser = GetAccountSerializer(user, many=True)
    if not user:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(ser.data, status=status.HTTP_200_OK)


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
