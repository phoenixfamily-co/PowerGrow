from django.http import HttpResponse
from django.template import loader
from flask import Response
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from About.models import AboutUs
from Calendar.models import Day
from PowerGrow.decorators import session_auth_required
from Product.models import Course
from Seo.models import News
from Seo.serializer import NewsSerializer
from PowerGrow.permissions import *


@session_auth_required
def manager_news_view(request):
    about = AboutUs.objects.values().first()
    news = News.objects.all().order_by('-pk')
    template = loader.get_template('manager/news.html')
    context = {
        "news": news,
        "about": about,
    }
    return HttpResponse(template.render(context, request))


@session_auth_required
def admin_news_view(request):
    about = AboutUs.objects.values().first()
    news = News.objects.all().order_by('-pk')
    template = loader.get_template('admin/news.html')
    context = {
        "news": news,
        "about": about,
    }
    return HttpResponse(template.render(context, request))


@session_auth_required
def teacher_news_view(request):
    about = AboutUs.objects.values().first()
    news = News.objects.all().order_by('-pk')
    template = loader.get_template('teacher/news.html')
    context = {
        "news": news,
        "about": about,
    }
    return HttpResponse(template.render(context, request))


@session_auth_required
def user_news_view(request):
    about = AboutUs.objects.values().first()
    news = News.objects.all().order_by('-pk')
    template = loader.get_template('user/news.html')
    context = {
        "news": news,
        "about": about,
    }
    return HttpResponse(template.render(context, request))


class NewsApi(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAdminUserOrStaff]


