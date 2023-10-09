from django.urls import path
from Reservation.views import *


app_name = 'reservation'

urlpatterns = [

    path('', reservation_view, name='reservation'),
    path('api/reserve/', ReservationView.as_view({'post': 'create', 'get': 'list'}), name='reserve'),
    path('api/gym/', GymView.as_view({'post': 'create', 'get': 'list'}), name='gym'),
    path('api/dates/<int:pk>/', DateView.as_view({'post': 'create', 'get': 'list'}), name='dates'),
    path('api/times/<int:pk>/', TimeView.as_view({'post': 'create', 'get': 'list'}), name='times'),
    path('transaction/<int:pk>/<str:day>/<str:time>/<int:duration>/', transaction_view, name='transaction'),
    path('successful/<int:pk>/<str:day>/<str:time>/<int:duration>/', successful_view, name='successful'),

]
