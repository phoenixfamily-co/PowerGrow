from django.urls import path
from Reservation.views import *


app_name = 'seo'

urlpatterns = [

    path('api/news/', ReservationView.as_view({'post': 'create', 'get': 'list'}), name='news'),

]
