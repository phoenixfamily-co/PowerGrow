from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from rest_framework import viewsets

from About.models import AboutUs
from PowerGrow.decorators import *
from Seo.models import News
from Seo.serializer import NewsSerializer
from PowerGrow.permissions import *


@session_staff_required
def manager_news_view(request):
    about = AboutUs.objects.first()

    if request.user.is_authenticated:
        news_items = News.objects.all()
        for news in news_items:
            news.users_who_read.add(request.user)
            news.save()

    news_items = News.objects.all().order_by('-pk')

    # پیاده‌سازی pagination
    paginator = Paginator(news_items, 100)
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
    return render(request, 'manager/news.html', context)


@session_admin_required
def admin_news_view(request):
    about = AboutUs.objects.first()

    if request.user.is_authenticated:
        news_items = News.objects.all()
        for news in news_items:
            news.users_who_read.add(request.user)
            news.save()

    news_items = News.objects.all().order_by('-pk')

    # پیاده‌سازی pagination
    paginator = Paginator(news_items, 100)
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
    return render(request, 'admin/news.html', context)


@session_teacher_required
def teacher_news_view(request):
    about = AboutUs.objects.values().first()

    if request.user.is_authenticated:
        news_items = News.objects.all()
        for news in news_items:
            news.users_who_read.add(request.user)
            news.save()

    news_items = News.objects.all().order_by('-pk')

    context = {
        "news": news_items,
        "about": about,
    }
    return render(request, 'user/news.html', context)



@session_auth_required
def user_news_view(request):
    about = AboutUs.objects.values().first()

    if request.user.is_authenticated:
        news_items = News.objects.all()
        for news in news_items:
            news.users_who_read.add(request.user)
            news.save()

    news_items = News.objects.all().order_by('-pk')

    context = {
        "news": news_items,
        "about": about,
    }
    return render(request, 'user/news.html', context)


class NewsApi(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAdminUserOrStaff]


