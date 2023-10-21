from django.urls import path
from User.views import *


app_name = 'user'


urlpatterns = [

    path('', login_view, name='login'),
    path('login/api/', CustomObtainAuthToken.as_view(), name='token_obtain_pair'),
    path('register/', register_view, name='register'),
    path('register/manager', register_manager_view, name='register_manager'),
    path('register/api/', RegisterView.as_view(), name="api_register"),
    path('register/manager/api/', AdminRegisterUser.as_view({'post': 'create', 'get': 'list'}), name="api_register"),
    path('verification/<str:number>/', verification_view, name='verification'),
    path('verification/api/<str:number>/', get_verification, name="api_verification"),
    path('verification/api/<str:number>/activate/', ActivateAccount.as_view(), name='activate_account'),
    path('forget/', forget_view, name="forget"),
    path('forget/api/<str:number>/', get_user, name="api_forget"),
    path('verification/password/<str:number>/', pass_view, name='password'),
    path('verification/password/api/<str:number>/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('update/<str:number>/', UpdateProfile.as_view(), name='update_profile'),
    path('delete/<str:number>/', DeleteAccount.as_view(), name='delete_profile'),
    path('get/<str:number>/', GetAccount.as_view(), name='get_profile'),
    path('all/', GetAllAccount.as_view(), name='get_all_profiles'),
    path('access/<str:number>/', ManagePermission.as_view(), name='manage_permission'),
    path('home/user/', user_home_view, name='user_home'),
    path('home/teacher/', teacher_home_view, name='teacher_home'),
    path('home/admin/', secretary_home_view, name='admin_home'),
    path('home/manager/', manager_home_view, name='manager_home'),
    path('profile/manager/', manager_profile_view, name='manager_profile'),
    path('profile/admin/', secretary_profile_view, name='admin_profile'),
    path('profile/teacher/', teacher_profile_view, name='teacher_profile'),
    path('profile/user/', user_profile_view, name='user_profile'),
]
