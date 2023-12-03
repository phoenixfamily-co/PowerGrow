from django.urls import path
from Reservation.views import *


app_name = 'reservation'

urlpatterns = [

    path('', reservation_view, name='reservation'),
    path('api/reserve/', ReservationView.as_view({'post': 'create', 'get': 'list'}), name='reserve'),
    path('api/admin/reserve/<int:time>/', ManagerAddReservationView.as_view({'post': 'create', 'get': 'list'}),
         name='admin-reserve'),
    path('api/admin/reserve/<int:time>/<int:pk>/', ManagerAddReservationView.as_view({'delete': 'destroy'}),
         name='delete-admin-reserve'),
    path('api/gym/', GymView.as_view({'post': 'create', 'get': 'list'}), name='gym'),
    path('transaction/<int:gym>/<int:time>/<int:session>/<str:holiday>/', transaction_view, name='transaction'),
    path('successful/<int:gym>/<int:time>/<int:session>/<str:holiday>/', successful_view, name='successful'),
    path('request/<int:amount>/', send_request, name='request'),
    path('verify/', verify , name='verify'),


]
