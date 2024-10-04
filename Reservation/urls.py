from django.urls import path
from Reservation.views import *
from Home.views import *


app_name = 'reservation'

urlpatterns = [

    path('', reservation_view, name='reservation'),
    path('reserve/', reserve_view, name='reserve_view'),
    path('reserve/admin/', admin_reserve_view, name='reserve_view_admin'),
    path('reserve/user/<int:pk>/', user_reserves_view, name='reserve_view_user'),
    path('api/reserve/', ReservationView.as_view({'post': 'create'}), name='reserve'),
    path('api/admin/reserve/<int:time>/<str:user>', ManagerAddReservationView.as_view({'post': 'create'}),
         name='admin-reserve'),
    path('api/admin/reserve/<int:time>/<int:pk>/delete', ManagerAddReservationView.as_view({'delete': 'destroy'}),
         name='delete-admin-reserve'),

    path('api/admin/reserve/<int:time>/<int:pk>/update/', ManagerAddReservationView.as_view({'put': 'update'}),
         name='update-admin-reserve'),

    path('api/gym/create/', GymView.as_view({'post': 'create'}), name='create_gym'),
    path('api/gym/update/<int:pk>/', GymView.as_view({'put': 'update'}), name='update_gym'),
    path('api/gym/delete/<int:pk>', GymView.as_view({'delete': 'destroy'}), name='delete_gym'),
    path('api/gym/', GymView.as_view({'get': 'list'}), name='gym'),
    path('gym/', gym_view, name='gym_view'),
    path('gym/admin/', admin_gym_view, name='gym_view_admin'),
    path('transaction/<int:gym>/<int:time>/<int:session>/<str:holiday>/', transaction_view, name='transaction'),
    path('verify/', verify, name='verify'),
    path('generate/pdf/<int:pk>/<int:end>/', generate_pdf_file, name='generate_pdf'),
]
