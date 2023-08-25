from django.urls import path
from Product import views

app_name = 'product'

urlpatterns = [
    path('product/', views.product_view, name='product'),
    path('catagory/', views.sport_view, name='sports')
]
