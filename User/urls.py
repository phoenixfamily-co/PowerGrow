from django.urls import path
from User.views import *


app_name = 'user'


urlpatterns = [

    path('login/', login_view, name='login'),
    path('login/api/', custom_login, name='login_api'),
    path('logout/api/', custom_logout, name='logout_api'),  # ثبت ویو logout
    path('register/', register_view, name='register'),
    path('register/api/', UserCreateView.as_view(), name='create-user'),  # ثبت‌نام و به‌روزرسانی پروفایل
    path('forget/', forget_view, name="forget"),
    path('verification/password/<str:number>/', pass_view, name='password'),
    path('home/user/<int:pk>/', user_home_view, name='user_home'),
    path('home/teacher/<int:pk>/', teacher_home_view, name='teacher_home'),
    path('home/admin/<int:pk>/', admin_home_view, name='admin_home'),
    path('home/manager/<int:pk>/', manager_home_view, name='manager_home'),
    path('teacher-profile/', teacher_profile_view, name='teacher_profile'),
    path('user-profile/', user_profile_view, name='user_profile'),
    path('salary/<int:pk>/', salary_view, name='salary'),
    path('home/manager/users/', manager_users_view, name='manager_users_view'),
    path('home/admin/users/', admin_users_view, name='admin_users_view'),
    path('update/user/<int:user_id>/', UserView.as_view({'put': 'update'}), name='user-update'),  # حذف کاربر
    path('delete/user/<int:user_id>/', UserView.as_view({'delete': 'destroy'}), name='user-delete'),  # حذف کاربر

    path('update/profile/', ProfileView.as_view({'put': 'update'}), name='update_profile'),

    path('change-password/<int:user_id>/', ChangePasswordView.as_view(), name='change-password'),
    path('profile/change-password/', ChangeProfilePasswordView.as_view(), name='change-profile-password'),

    path('change-access/<int:user_id>/', ChangeUserAccessView.as_view(), name='change-user-access'),
    path('change-salary/<int:user_id>/', ChangeUserSalaryView.as_view(), name='change-user-salary'),
    path('change-number/<int:user_id>/', ChangeNumberView.as_view(), name='change-user-number'),
    path('search/api/', UserSearchView.as_view(), name='user-search'),  # مسیر جستجو

]
