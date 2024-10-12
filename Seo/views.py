from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from rest_framework import viewsets

from About.models import AboutUs
from PowerGrow.decorators import *
from Seo.models import News
from Seo.serializer import NewsSerializer
from PowerGrow.permissions import *


@session_staff_required
def manager_news_view(request):
    about = AboutUs.objects.first()
    news = News.objects.all().order_by('-pk')

    # پیاده‌سازی pagination
    paginator = Paginator(news, 100)
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
    return render(request, 'manager/news.html', context)


@session_admin_required
def admin_news_view(request):
    about = AboutUs.objects.first()
    news = News.objects.all().order_by('-pk')

    # پیاده‌سازی pagination
    paginator = Paginator(news, 100)
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

    # بررسی اینکه آیا کاربر اخبار را خوانده است یا نه
    if request.user.is_authenticated:
        if not request.session.get('has_read_news'):
            for item in news:
                if item.is_new_for_user(request.user):
                    item.users_who_read.add(request.user)
                    item.save()
            request.session['has_read_news'] = True

    # ایجاد یک لیست جدید برای ارسال به قالب
    new_news_items = []
    for item in news:
        new_news_items.append({
            'item': item,
            'is_new': item.is_new_for_user(request.user)
        })

    context = {
        "news": new_news_items,
        "about": about,
    }
    return render(request, 'user/news.html', context)


class NewsApi(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAdminUserOrStaff]


