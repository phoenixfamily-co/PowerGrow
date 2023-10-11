from django.urls import path
from Reservation.views import *


app_name = 'reservation'

urlpatterns = [

    path('', reservation_view, name='reservation'),
    path('api/reserve/', ReservationView.as_view({'post': 'create', 'get': 'list'}), name='reserve'),
    path('api/gym/', GymView.as_view({'post': 'create', 'get': 'list'}), name='gym'),
    path('transaction/<int:pk>/<str:day>/<str:time>/<int:session>/<str:holiday>/', transaction_view, name='transaction'),
    path('successful/<int:pk>/<str:day>/<str:time>/<int:session>/<str:holiday>/', successful_view, name='successful'),

]
