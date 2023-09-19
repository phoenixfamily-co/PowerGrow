from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny

from User.models import User
from User.serializer import RegisterSerializer, ChangePasswordSerializer, UpdateProfileSerializer, \
    DeleteAccountSerializer, GetAccountSerializer, ManagePermissionSerializer


def login_view(request):
    return render(request, "login.html")


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


class GetAccount(generics.ListAPIView, ):
    queryset = User.objects.all()
    lookup_field = "number"
    permission_classes = (AllowAny,)
    serializer_class = GetAccountSerializer

    def get_queryset(self):
        return User.objects.filter(number=self.kwargs['number'])


class GetAllAccount(generics.ListCreateAPIView, ):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = GetAccountSerializer


class ManagePermission(generics.UpdateAPIView, ):
    queryset = User.objects.all()
    lookup_field = "number"
    permission_classes = (AllowAny,)
    serializer_class = ManagePermissionSerializer
