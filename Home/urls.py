from django.urls import path
from Home import views

app_name = 'home'

urlpatterns = [
    path('', views.home_view, name='home'),
]
