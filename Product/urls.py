from django.urls import path
from Product.views import *

app_name = 'product'

urlpatterns = [
    path('<int:pk>/<int:session>/<int:day>/', product_view, name='product'),
    path('api/course/create/', CourseView.as_view({'post': 'create'}), name='create_courses'),
    path('api/course/', CourseView.as_view({'post': 'create', 'get': 'list'}), name='courses'),
    path('course/', courses_view, name='courses_view'),
    path('api/course/<int:pk>/', CourseView.as_view({'delete': 'destroy'}), name='delete-courses'),
    path('api/participate/', ParticipationView.as_view({'post': 'create', 'get': 'list'}), name='participate'),
    path('api/admin/participate/<int:pk>/', ManagerParticipationView.as_view({'delete': 'destroy'}),
         name='delete-admin-participate'),
    path('api/admin/participate/', ManagerParticipationView.as_view({'post': 'create', 'get': 'list'}),
         name='admin-participate'),
    path('api/search/<int:pk>/', SearchView.as_view(), name='search'),
    path('api/days/', DaysView.as_view({'post': 'create'}), name='create_days'),
    path('api/days/<int:pk>/', DaysView.as_view({'get': 'list'}), name='days'),
    path('api/sessions/', SessionView.as_view({'post': 'create'}), name='creat_sessions'),
    path('api/sessions/<int:pk>/', SessionView.as_view({'get': 'list'}), name='sessions'),
    path('sport/<int:pk>/', category_view, name='category'),
    path('sports/', sports_view, name='sports_view'),
    path('api/sport/create/', SportView.as_view({'post': 'create'}), name='create_sports'),
    path('api/sport/', SportView.as_view({'post': 'create', 'get': 'list'}), name='sports'),
    path('payment/<int:pk>/<int:session>/<int:day>/', payment_view, name='payment'),
    path('check/<int:pk>/<int:session>/<int:day>/', check_view, name='check'),
    path('api/participants/<int:pk>/', CourseUserView.as_view(), name='course_user'),

]
