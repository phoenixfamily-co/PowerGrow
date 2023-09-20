from django.urls import path
from User.views import RegisterView, ChangePasswordView, login_view, UpdateProfile, DeleteAccount, GetAccount, \
    GetAllAccount, ManagePermission, register_view, verification_view, home_view, forget_view, pass_view, get_selected

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name = 'user'


urlpatterns = [

    path('login/', login_view, name='login'),
    path('login/api/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register_view, name='register'),
    path('register/api/', RegisterView.as_view(), name="api_register"),
    path('verification/', verification_view, name='verification'),
    path('verification/api/', RegisterView.as_view(), name="api_verification"),
    path('forget/', forget_view, name="forget"),
    path('forget/api/<str:number>/', get_selected, name="api_forget"),
    path('password/<str:number>/', pass_view, name='password'),
    path('password/api/<str:number>/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('update/<str:number>/', UpdateProfile.as_view(), name='update_profile'),
    path('delete/<str:number>/', DeleteAccount.as_view(), name='delete_profile'),
    path('get/<str:number>/', GetAccount.as_view(), name='get_profile'),
    path('all/', GetAllAccount.as_view(), name='get_all_profiles'),
    path('access/<str:number>/', ManagePermission.as_view(), name='manage_permission'),
    path('home/', home_view, name='home'),

]
