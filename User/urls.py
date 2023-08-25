from django.urls import path
from User import views


app_name = 'user'

urlpatterns = [

    path('', views.login_view, name='login'),
]
