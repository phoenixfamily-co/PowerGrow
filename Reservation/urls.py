from django.urls import path
from Reservation import views


app_name = 'reservation'

urlpatterns = [

    path('', views.reservation_view, name='reservation')

]
