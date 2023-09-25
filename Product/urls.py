from django.urls import path
from Product.views import CourseView, sport_view, product_view, DaysView , SportView, SessionView

app_name = 'product'

urlpatterns = [
    path('<int:pk>/<int:session>/<int:day>/', product_view, name='product'),
    path('api/course/', CourseView.as_view({'post': 'create', 'get': 'list'}), name='courses'),
    path('api/day/', DaysView.as_view({'post': 'create', 'get': 'list'}), name='days'),
    path('api/session/', SessionView.as_view({'post': 'create', 'get': 'list'}), name='days'),
    path('sport/<int:category>', sport_view, name='category'),
    path('api/sport/', SportView.as_view({'post': 'create', 'get': 'list'}), name='sports'),

]
