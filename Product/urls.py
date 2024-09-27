from django.urls import path
from Product.views import *

app_name = 'product'

urlpatterns = [
    path('categories/<int:pk>/', category_view, name='category_view'),
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
    path('manager/users/<int:pk>/', manager_user_list, name='manager_user_list'),
    path('teacher/users/<int:pk>/<int:user>/', teacher_user_list, name='teacher_user_list'),

    path('api/sports/', SportListCreateView.as_view(), name='sport-list-create'),
    path('api/sports/<int:pk>/', SportDetailView.as_view(), name='sport-detail'),

    path('api/courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('api/courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),

    path('api/days/', DaysListCreateView.as_view(), name='day-list-create'),
    path('api/days/<int:pk>/', DaysDetailView.as_view(), name='day-detail'),

    path('api/sessions/', SessionListCreateView.as_view(), name='sessions-list-create'),
    path('api/sessions/<int:pk>/', SessionDetailView.as_view(), name='session-detail'),

    path('api/participations/', ParticipationCreateView.as_view(), name='create-participation'),
    path('api/manager/participations/',
         ManagerParticipationView.as_view({'post': 'create', 'put': 'update', 'delete': 'destroy'}),
         name='manager-participation'),

    path('get-days-for-session/', get_days_for_session, name='get_days_for_session'),
]
