from django.urls import path
from User.views import *


app_name = 'user'


urlpatterns = [

    path('', login_view, name='login'),
    path('login/api/', CustomObtainAuthToken.as_view(), name='token_obtain_pair'),
    path('register/', register_view, name='register'),
    path('register/api/', RegisterView.as_view(), name="api_register"),
    path('register/manager/api/', AdminRegisterUser.as_view({'post': 'create'}), name="admin_register"),
    path('register/secretary/api/', SecretaryRegisterUser.as_view({'post': 'create'}), name="secretary_register"),
    path('verification/<str:number>/', verification_view, name='verification'),
    path('verification/api/<str:number>/', get_verification, name="api_verification"),
    path('verification/api/<str:number>/activate/', ActivateAccount.as_view(), name='activate_account'),
    path('forget/', forget_view, name="forget"),
    path('forget/api/<str:number>/', get_user, name="api_forget"),
    path('verification/password/<str:number>/', pass_view, name='password'),
    path('verification/password/api/<str:number>/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('salary/api/<str:number>/', ChangeSalaryView.as_view(), name='change_salary'),
    path('debt/api/<str:number>/', ChangeDebtView.as_view(), name='change_debt'),
    path('update/<str:number>/', UpdateProfile.as_view(), name='update_profile'),
    path('delete/<int:id>/', DeleteAccount.as_view(), name='delete_profile'),
    path('get/<str:number>/', GetAccount.as_view(), name='get_profile'),
    path('all/', GetAllAccount.as_view(), name='get_all_profiles'),
    path('access/<str:number>/', ManagePermission.as_view(), name='manage_access'),
    path('access/<str:number>/secretary/', ManageAccess.as_view(), name='manage_access_secretary'),
    path('home/user/<int:pk>/', user_home_view, name='user_home'),
    path('home/teacher/<int:pk>/', teacher_home_view, name='teacher_home'),
    path('home/admin/<int:pk>/', secretary_home_view, name='admin_home'),
    path('home/manager/<int:pk>/', manager_home_view, name='manager_home'),
    path('profile/<int:pk>/', profile_view, name='profile'),
    path('reservation/<int:pk>/', user_gym_view, name='user_gym'),
    path('participants/<int:pk>/', user_course_view, name='user_course'),
    path('users/', user_view, name='users_view'),
    path('users/admin/', admin_user_view, name='users_view_admin'),

]
