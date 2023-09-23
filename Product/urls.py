from django.urls import path
from Product.views import CourseView, sport_view, product_view, DaysView

app_name = 'product'

urlpatterns = [
    path('api/course/', CourseView.as_view({'post': 'create', 'get': 'list'}), name='courses'),
    path('api/day/', DaysView.as_view({'post': 'create'}), name='days'),
    path('<int:pk>/<int:session>/<int:day>/', product_view, name='product'),
    path('category/', sport_view, name='category'),
]
