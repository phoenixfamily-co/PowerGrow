from django.urls import path
from User.views import RegisterView, ChangePasswordView, login_view, UpdateProfile, DeleteAccount, GetAccount,\
    GetAllAccount, ManagePermission

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name = 'user'


urlpatterns = [

    path('', login_view, name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password/<str:number>/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('update/<str:number>/', UpdateProfile.as_view(), name='update_profile'),
    path('delete/<str:number>/', DeleteAccount.as_view(), name='delete_profile'),
    path('get/<str:number>/', GetAccount.as_view(), name='get_profile'),
    path('all/', GetAllAccount.as_view(), name='get_all_profiles'),
    path('access/<str:number>/', ManagePermission.as_view(), name='manage_permission'),

]
