from django.urls import path
from Product.views import *

app_name = 'product'

urlpatterns = [
    path('categories/<int:pk>/', category_view, name='category_view'),
    path('offer/', offer_view, name='offer_view'),

    path('products/<int:pk>/', product_view, name='product_view'),
    path('payment/<int:pk>/<int:session>/<int:day>/<int:start>/', payment_view, name='payment_view'),
    path('verify/', verify, name='verify'),
    path('manager/sports/', manager_sports_view, name='manager_sports'),
    path('admin/sports/', admin_sports_view, name='admin_sports'),
    path('manager/courses/', manager_courses_view, name='manager_courses'),
    path('admin/courses/', admin_courses_view, name='admin_courses'),
    path('teacher/courses/<int:pk>/', teacher_courses_view, name='teacher_courses'),
    path('user/courses/<int:pk>/', user_courses_view, name='user_courses'),
    path('manager/sessions/', manager_session_view, name='manager_sessions'),
    path('admin/sessions/', admin_session_view, name='admin_sessions'),
    path('manager/days/', manager_days_view, name='manager_days'),
    path('admin/days/', admin_days_view, name='admin_days'),
    path('manager/offers/', manager_offers_view, name='manager_offers'),
    path('admin/offers/', admin_offers_view, name='admin_offers'),
    path('manager/users/<int:pk>/', manager_user_list, name='manager_user_list'),
    path('admin/users/<int:pk>/', admin_user_list, name='admin_user_list'),
    path('teacher/users/<int:pk>/', teacher_user_list, name='teacher_user_list'),
    path('course/update/<int:pk>/', update_course, name='update_course'),
    path('session/update/<int:pk>/', update_session, name='update_session'),
    path('participants/create/<int:course_id>/', create_participants, name='create-participant'),  # URL برای نمایش فرم
    path('participants/update/<int:participant_id>/', update_participant_view, name='update-participant'),
    path('off/create/',create_off_view, name='create-off'),
    path('api/sports/', SportListCreateView.as_view(), name='manager-create-sport'),
    path('api/sports/update/<int:pk>/', SportDetailView.as_view({'put': 'update'}), name='manager-update-sport'),
    path('api/sports/delete/<int:pk>/', SportDetailView.as_view({'delete': 'destroy'}), name='manager-delete-sport'),

    path('api/courses/', CourseListCreateView.as_view(), name='manager-create-course'),
    path('api/courses/update/<int:pk>/', CourseDetailView.as_view({'put': 'update'}), name='manager-update-course'),
    path('api/courses/delete/<int:pk>/', CourseDetailView.as_view({'delete': 'destroy'}), name='manager-delete-course'),

    path('api/days/', DaysListCreateView.as_view(), name='manager-create-day'),
    path('api/days/update/<int:pk>/', DaysDetailView.as_view({'put': 'update'}), name='manager-update-day'),
    path('api/days/delete/<int:pk>/', DaysDetailView.as_view({'delete': 'destroy'}), name='manager-delete-day'),

    path('api/sessions/', SessionListCreateView.as_view(), name='manager-create-session'),
    path('api/sessions/update/<int:pk>/', SessionDetailView.as_view({'put': 'update'}), name='manager-update-session'),
    path('api/sessions/delete/<int:pk>/', SessionDetailView.as_view({'delete': 'destroy'}),
         name='manager-delete-session'),

    path('api/participations/', ParticipationCreateView.as_view({'post': 'create'}), name='create-participation'),
    path('api/manager/participations/<int:course>/',
         ManagerParticipationView.as_view({'post': 'create'}),
         name='manager-create-participation'),
    path('api/manager/participations/update/<int:pk>/',
         ManagerParticipationView.as_view({'put': 'update'}),
         name='manager-update-participation'),
    path('api/manager/participations/delete/<int:pk>/',
         ManagerParticipationView.as_view({'delete': 'destroy'}),
         name='manager-delete-participation'),
    path('get-days-for-session/', get_days_for_session, name='get_days_for_session'),

    path('change-price/<int:day_id>/', ChangeDayPriceView.as_view(), name='change-day-price'),

    path('api/offer/', OfferView.as_view({'post': 'create'}), name='create-offer'),

    path('api/offer/delete/<int:pk>/', OfferView.as_view({'delete': 'destroy'}), name='delete-offer'),

    path('api/change-day-salary/', UpdateAllParticipantsDaysAPIView.as_view(), name='change-day-salary'),

]
