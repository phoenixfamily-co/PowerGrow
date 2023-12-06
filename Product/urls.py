from django.urls import path
from Product.views import *

app_name = 'product'

urlpatterns = [
    path('api/sport/create/', SportView.as_view({'post': 'create'}), name='create_sports'),
    path('api/sport/delete/<int:pk>/', SportView.as_view({'delete': 'destroy'}), name='delete-sports'),
    path('api/sport/', SportView.as_view({'get': 'list'}), name='sports'),
    path('sport/<int:pk>/', category_view, name='category'),
    path('sports/', sports_view, name='sports_view'),
    path('api/course/create/', CourseView.as_view({'post': 'create'}), name='create_courses'),
    path('api/course/delete/<int:pk>/', CourseView.as_view({'delete': 'destroy'}), name='delete-courses'),
    path('api/course/update/<int:pk>/', CourseView.as_view({'put': 'update'}), name='update-courses'),
    path('api/course/', CourseView.as_view({'get': 'list'}), name='courses'),
    path('course/', courses_view, name='courses_view'),
    path('api/sessions/create/', SessionView.as_view({'post': 'create'}), name='creat_sessions'),
    path('api/sessions/delete/<int:pk>/', SessionView.as_view({'delete': 'destroy'}), name='delete_sessions'),
    path('api/sessions/<int:pk>/', SessionView.as_view({'get': 'list'}), name='sessions'),
    path('api/sessions/', session_view, name='sessions_view'),
    path('api/days/create/', DaysView.as_view({'post': 'create'}), name='create_days'),
    path('api/days/delete/<int:pk>/', DaysView.as_view({'delete': 'destroy'}), name='delete-days'),
    path('api/days/<int:pk>/', DaysView.as_view({'get': 'list'}), name='days'),
    path('api/days/', day_view, name='days-view'),
    path('api/participate/', ParticipationView.as_view({'post': 'create', 'get': 'list'}), name='participate'),
    path('api/admin/participate/<int:pk>/delete/', ManagerParticipationView.as_view({'delete': 'destroy'}),
         name='delete-admin-participate'),
    path('api/admin/participate/<int:id>/create/', ManagerParticipationView.as_view({'post': 'create'}),
         name='create-admin-participate'),
    path('api/admin/participate/', ManagerParticipationView.as_view({'get': 'list'}),
         name='admin-participate'),
    path('api/search/<int:pk>/', SearchView.as_view(), name='search'),
    path('payment/<int:pk>/<int:session>/<int:day>/', payment_view, name='payment'),
    path('check/<int:pk>/<int:session>/<int:day>/', check_view, name='check'),
    path('api/participants/<int:pk>/', CourseUserView.as_view(), name='course_user'),
    path('<int:pk>/<int:session>/<int:day>/', product_view, name='product'),
]