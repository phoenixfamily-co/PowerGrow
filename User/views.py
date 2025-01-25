import json

from django.contrib.auth import login, authenticate, logout, get_user_model
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.generics import get_object_or_404, UpdateAPIView

from About.models import AboutUs
from PowerGrow.decorators import *
from Product.models import *
from Seo.models import News
from User.serializer import *
from rest_framework import status, viewsets, generics, filters
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from PowerGrow.permissions import *

User = get_user_model()


@csrf_exempt
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


@csrf_exempt
def custom_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            number = data.get('username')  # دریافت شماره به عنوان username
            password = data.get('password')

            # بررسی وجود کاربر با استفاده از number
            user = User.objects.get(number=number)

            # اعتبارسنجی پسورد
            user = authenticate(request, username=number, password=password)
            if user is not None:
                login(request, user)
                user_data = {
                    'id': user.id,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser,
                    'is_teacher': user.is_teacher,
                }
                return JsonResponse({'status': 'success', 'user': user_data}, status=200)
            else:
                return JsonResponse({'error': 'پسورد اشتباه است'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'error': 'نام کاربری وجود ندارد'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'فرمت JSON نامعتبر است'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def custom_logout(request):
    logout(request)  # خروج کاربر

    return redirect('user:login')


@csrf_exempt
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


@session_auth_required
def user_home_view(request, pk):
    about = AboutUs.objects.values().first()
    template = loader.get_template('user/dashboard.html')
    user = get_object_or_404(User, id=pk)
    news_items = News.objects.all()
    unread_news = [news for news in news_items if news.is_new_for_user(request.user)]

    context = {
        "about": about,
        "user": user,
        'unread_news_count': len(unread_news),
    }

    return HttpResponse(template.render(context, request))


@session_teacher_required
def teacher_home_view(request, pk):
    about = AboutUs.objects.values().first()
    template = loader.get_template('teacher/dashboard.html')
    user = get_object_or_404(User, id=pk)
    news_items = News.objects.all()
    unread_news = [news for news in news_items if news.is_new_for_user(request.user)]

    context = {
        "about": about,
        "user": user,
        'unread_news_count': len(unread_news),

    }
    return HttpResponse(template.render(context, request))


@session_admin_required
def admin_home_view(request, pk):
    about = AboutUs.objects.values().first()
    template = loader.get_template('admin/dashboard.html')
    user = get_object_or_404(User, id=pk)
    news_items = News.objects.all()
    unread_news = [news for news in news_items if news.is_new_for_user(request.user)]

    context = {
        "about": about,
        "user": user,
        'unread_news_count': len(unread_news),

    }
    return HttpResponse(template.render(context, request))


@session_staff_required
def manager_home_view(request, pk):
    about = AboutUs.objects.values().first()
    template = loader.get_template('manager/dashboard.html')
    user = get_object_or_404(User, id=pk)
    news_items = News.objects.all()
    unread_news = [news for news in news_items if news.is_new_for_user(request.user)]

    context = {
        "about": about,
        "user": user,
        'unread_news_count': len(unread_news),
    }

    return HttpResponse(template.render(context, request))


@session_teacher_required
def teacher_profile_view(request):
    about = AboutUs.objects.values().first()
    template = loader.get_template('teacher/profile.html')
    user = request.user
    context = {
        "about": about,
        "user": user
    }
    return HttpResponse(template.render(context, request))


@session_auth_required
def user_profile_view(request):
    about = AboutUs.objects.values().first()
    template = loader.get_template('user/profile.html')
    user = request.user
    context = {
        "about": about,
        "user": user
    }
    return HttpResponse(template.render(context, request))


@session_teacher_required
def salary_view(request, pk):
    about = AboutUs.objects.values().first()
    template = loader.get_template('teacher/salary.html')
    user = get_object_or_404(User, id=pk)

    # گرفتن آی‌دی دوره‌هایی که مربی در آن‌ها شرکت دارد
    course_ids = Participants.objects.filter(user=user).values_list('course_id', flat=True)
    participants_ids = Participants.objects.filter(course_id__in=course_ids)

    # گرفتن همه دوره‌های مربی
    courses = Course.objects.filter(id__in=course_ids)

    # متغیر برای ذخیره حقوق کلی و تعداد کل شرکت‌کننده‌ها
    total_salary = 0
    total_participants_count = 0
    total_news = 0
    course_data = []

    calculated_participant_data = []

    for course in courses:
        # گرفتن شرکت‌کننده‌های این دوره که مربی است
        participant_teacher = Participants.objects.filter(user=user, course=course).first()

        if not participant_teacher:
            continue  # اگر مربی اطلاعاتی در این دوره ندارد، عبور کند

        participant_session = participant_teacher.session.number

        teacher_start_day_id = participant_teacher.startDay_id
        teacher_end_day_id = participant_teacher.endDay_id

        # فیلتر شرکت‌کننده‌های این دوره بر اساس تاریخ شروع و پایان مربی
        participants = Participants.objects.filter(
            course=course,
            user__is_teacher=False,
            user__is_superuser=False,
            user__is_staff=False,
            price__gt=0,
            success=True,
            startDay_id__gte=teacher_start_day_id,
            startDay_id__lte=teacher_end_day_id
        )

        for participant in participants:
            calculated_participant_data.append({
                "id": participant.pk,
                "name": participant.user.name,
                "price": participant.price
            })

        # تعداد شرکت‌کننده‌های این دوره
        participants_count = participants.count()

        # جمع قیمت‌های شرکت‌کننده‌های این دوره
        total_price = participants.aggregate(total_price=Sum('price'))['total_price'] or 0

        if user.salary == "ثابت":
            # حقوق ثابت
            salary = user.fee * participant_session

            # فیلتر کردن اخبار کنسلی دوره
            cancelled_news = News.objects.filter(
                course=course,
                title="کنسلی",
                date__id__gte=teacher_start_day_id,
                date__id__lte=teacher_end_day_id
            )

            total_news = cancelled_news.count()

            # کاهش از حقوق برای اخبار کنسلی
            for news in cancelled_news:
                salary -= user.fee  # از حقوق ثابت کم کنید

            total_salary += salary

        elif user.salary == "درصدی":
            percentage = user.fee
            salary = total_price * percentage / 100
            total_salary += salary
            total_participants_count += participants_count  # جمع تعداد کل شرکت‌کننده‌ها
        else:
            salary = 0
            total_salary = 0

        # ذخیره اطلاعات دوره و حقوق مربوط به آن
        course_data.append({
            "course": course,
            "participants_count": participants_count,
            "total_price": total_price,
            "salary": salary
        })

    if user.situation == "بدهکار":
        total_salary = total_salary - user.debt
    elif user.situation == "پستانکار":
        total_salary = total_salary + user.debt

    context = {
        "about": about,
        "user": user,
        "courses": course_data,  # اطلاعات حقوق و شرکت‌کننده‌ها برای هر دوره
        "total_salary": int(total_salary),  # حقوق کل مربی
        "total_participants_count": total_participants_count,  # تعداد کل شرکت‌کننده‌های محاسبه‌شده
        "total_courses": len(course_data),
        "total_participants": participants_ids.count(),
        "calculated_participant_data": calculated_participant_data,  # ارسال لیست به قالب
        "total_news": total_news,

    }

    return HttpResponse(template.render(context, request))


@session_staff_required
def manager_users_view(request):
    template = loader.get_template('manager/users.html')
    about = AboutUs.objects.values().first()
    user = User.objects.all().order_by('-datetime')
    p = Paginator(user, 150)  # ایجاد Paginator با queryset کاربران
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
        'page_obj': page_obj,
    }
    return HttpResponse(template.render(context, request))


@session_admin_required
def admin_users_view(request):
    template = loader.get_template('admin/users.html')
    about = AboutUs.objects.values().first()
    user = User.objects.all().order_by('-datetime')
    p = Paginator(user, 150)  # ایجاد Paginator با queryset کاربران
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


class UserCreateView(generics.CreateAPIView):
    queryset = Session.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if request.user.is_authenticated:
                user.created = request.user  # مقداردهی فیلد created
                user.save()  # ذخیره تغییرات
            return Response({"message": "User registered successfully!", "user_id": user.id},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]  # برای ثبت‌نام، در ابتدا می‌توانیم AllowAny را قرار دهیم
    serializer_class = ManagerProfileSerializer  # برای ثبت‌نام

    def update(self, request, user_id):
        user = User.objects.get(id=user_id)  # کاربر فعلی
        serializer = self.serializer_class(user, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Profile updated successfully!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)  # پیدا کردن کاربر بر اساس ID
            user.delete()  # حذف کاربر
            return Response({"message": "User deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class ProfileView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]  # برای ثبت‌نام، در ابتدا می‌توانیم AllowAny را قرار دهیم
    serializer_class = UserProfileSerializer  # برای ثبت‌نام

    def update(self, request):
        user = self.request.user
        serializer = self.serializer_class(user, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Profile updated successfully!"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)  # پیدا کردن کاربر بر اساس ID
            user.delete()  # حذف کاربر
            return Response({"message": "User deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class ChangeNumberView(UpdateAPIView):
    serializer_class = ChangeNumberSerializer
    permission_classes = [IsAdminUserOrStaff]

    def get_object(self):
        user_id = self.kwargs['user_id']
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if user is None:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(user, data=request.data)  # Pass the existing user instance here
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Now it updates the existing user

        return Response({"detail": "نام کاربری با موفقیت تغییر کرد"}, status=status.HTTP_200_OK)


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # دریافت کاربر با استفاده از ID یا username از URL
        user_id = self.kwargs['user_id']
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if user is None:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_password = serializer.validated_data['new_password']

        user.set_password(new_password)
        user.save()
        return Response({"detail": "پسورد با موفقیت تغییر کرد"}, status=status.HTTP_200_OK)


class ChangeProfilePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = self.request.user
        if user is None:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        old_password = request.data.get("old_password")

        if not user.check_password(old_password):
            return Response({"detail": "پسورد فعلی اشتباه است."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_password = serializer.validated_data['new_password']

        user.set_password(new_password)
        user.save()
        return Response({"detail": "پسورد با موفقیت تغییر کرد"}, status=status.HTTP_200_OK)


class ChangeUserAccessView(UpdateAPIView):
    serializer_class = ChangeUserAccessSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        user_id = self.kwargs['user_id']
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if user is None:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(user, data=request.data)  # اضافه کردن partial=True برای بروزرسانی جزئی
        serializer.is_valid(raise_exception=True)
        serializer.save()  # از متد save سریالایزر استفاده می‌کنیم

        return Response({"detail": "User access has been updated successfully."}, status=status.HTTP_200_OK)


class ChangeUserSalaryView(UpdateAPIView):
    serializer_class = ChangeUserSalarySerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        user_id = self.kwargs['user_id']
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if user is None:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(user, data=request.data)  # اضافه کردن partial=True برای بروزرسانی جزئی
        serializer.is_valid(raise_exception=True)
        serializer.save()  # از متد save سریالایزر استفاده می‌کنیم

        return Response({"detail": "User access has been updated successfully."}, status=status.HTTP_200_OK)


class UserSearchView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'number']
