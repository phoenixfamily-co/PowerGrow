import json

from django.contrib.auth import login, authenticate, logout, get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from About.models import AboutUs
from Product.models import *
from User.serializer import *
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()


def login_view(request):
    about = AboutUs.objects.values().first()
    template = loader.get_template('public/login.html')
    sport = Sport.objects.all().values()
    context = {
        "about": about,
        "sport": sport,
    }
    if request.user.is_authenticated:
        if request.user.is_staff:
            # ریدایرکت به داشبورد ادمین
            return redirect(f'/user/home/manager/{request.user.id}/')

        elif request.user.is_superuser:
            return redirect(f'/user/home/admin/{request.user.id}/')

        elif request.user.is_teacher:
            return redirect(f'/user/home/teacher/{request.user.id}/')
        else:
            # ریدایرکت به داشبورد کاربر عادی
            return redirect(f'/user/home/user/{request.user.id}/')
    else:
        return HttpResponse(template.render(context, request))


def custom_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # داده‌ها از JSON خوانده می‌شوند
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser,
                    'is_teacher': user.is_teacher
                }
            }, status=200)
        return JsonResponse({'error': 'Invalid credentials'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def custom_logout(request):
    logout(request)  # خروج کاربر

    return redirect('user:login')


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


# def verification_view(request, number):
#     about = AboutUs.objects.values().first()
#     data = {'to': number}
#     response = requests.post('https://console.melipayamak.com/api/send/otp/d15bf0639e874ecebb5040b599cb8af6',
#                              json=data)
#     template = loader.get_template('public/verification.html')
#     context = {
#         "number": number,
#         "about": about,
#         "response": response.json()
#     }
#     return HttpResponse(template.render(context, request))


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
def teacher_home_view(request, pk):
    about = AboutUs.objects.values().first()
    template = loader.get_template('teacher/dashboard.html')
    user = User.objects.all().get(id=pk)
    context = {
        "about": about,
        "user": user
    }
    return HttpResponse(template.render(context, request))


@cache_page(60 * 15)
def secretary_home_view(request, pk):
    about = AboutUs.objects.values().first()
    template = loader.get_template('admin/dashboard.html')
    user = get_user_model()
    context = {
        "about": about,
        "user": user

    }
    return HttpResponse(template.render(context, request))


@cache_page(60 * 15)
def manager_home_view(request, pk):
    about = AboutUs.objects.values().first()
    template = loader.get_template('manager/dashboard.html')
    user = get_user_model()
    context = {
        "about": about,
        "user": user
    }
    return HttpResponse(template.render(context, request))


def profile_view(request, pk):
    about = AboutUs.objects.values().first()
    template = loader.get_template('public/profile.html')
    user = get_user_model()
    context = {
        "about": about,
        "user": user
    }
    return HttpResponse(template.render(context, request))


def salary_view(request, pk):
    about = AboutUs.objects.values().first()
    template = loader.get_template('teacher/salary.html')
    user = get_user_model()
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


def users_view(request):
    template = loader.get_template('manager/users.html')
    about = AboutUs.objects.values().first()
    user = User.objects.all()
    p = Paginator(user, 1000)  # ایجاد Paginator با queryset کاربران
    page_number = request.GET.get('page')

    try:
        page_obj = p.get_page(page_number)  # بازگشت صفحه مورد نظر
    except PageNotAnInteger:
        # اگر page_number عدد صحیح نباشد، صفحه اول را assign کن
        page_obj = p.page(1)
    except EmptyPage:
        # اگر صفحه خالی باشد، آخرین صفحه را برگردان
        page_obj = p.page(p.num_pages)

    context = {
        "about": about,
        'page_obj': page_obj
    }
    return HttpResponse(template.render(context, request))


class UserView(viewsets.ViewSet):
    permission_classes = (AllowAny,)  # برای ثبت‌نام، در ابتدا می‌توانیم AllowAny را قرار دهیم
    serializer_class = RegisterSerializer  # برای ثبت‌نام

    def post(self, request):
        # ثبت‌نام کاربر
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully!", "user_id": user.id},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        # به‌روزرسانی پروفایل کاربر
        self.permission_classes = (IsAuthenticated,)  # مجوزها برای به‌روزرسانی
        user = request.user  # کاربر فعلی
        profile_serializer = UserProfileSerializer(user, data=request.data)

        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response({"message": "Profile updated successfully!"}, status=status.HTTP_200_OK)

        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        # حذف کاربر (تنها برای مدیران)
        self.permission_classes = (IsAdminUser,)  # فقط مدیران می‌توانند کاربر را حذف کنند
        try:
            user = User.objects.get(id=user_id)  # پیدا کردن کاربر بر اساس ID
            user.delete()  # حذف کاربر
            return Response({"message": "User deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
