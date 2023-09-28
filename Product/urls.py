from django.urls import path
from Product.views import *

app_name = 'product'

urlpatterns = [
    path('<int:pk>/<int:session>/<int:day>/', product_view, name='product'),
    path('api/course/', CourseView.as_view({'post': 'create', 'get': 'list'}), name='courses'),
    path('api/participate/', ParticipationView.as_view({'post': 'create', 'get': 'list'}), name='participate'),
    path('api/search/<int:pk>/', SearchView.as_view(), name='search'),
    path('api/days/<int:pk>/', DaysView.as_view({'post': 'create', 'get': 'list'}), name='days'),
    path('api/sessions/<int:pk>/', SessionView.as_view({'post': 'create', 'get': 'list'}), name='sessions'),
    path('sport/<int:pk>/', sport_view, name='category'),
    path('api/sport/', SportView.as_view({'post': 'create', 'get': 'list'}), name='sports'),

]
