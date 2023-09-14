from django.urls import path
from Product import views

app_name = 'product'

urlpatterns = [
    path('<int:pk>', views.product_view, name='product'),
    path('category/', views.sport_view, name='category'),
    path('api/create', views.Create_Course.as_view({'post': 'create'}), name='create_product'),

]
