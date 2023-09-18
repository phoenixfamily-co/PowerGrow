from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny

from User.models import User
from User.serializer import RegisterSerializer


def login_view(request):
    return render(request, "login.html")


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
