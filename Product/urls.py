from django.urls import path
from Product import views

app_name = 'product'

urlpatterns = [
    path('', views.product_view, name='product'),
    path('category/', views.sport_view, name='category')
]
