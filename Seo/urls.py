from django.urls import path
from Seo.views import *


app_name = 'seo'

urlpatterns = [

    path('api/news/', NewsApi.as_view({'post': 'create', 'get': 'list'}), name='news'),
    path('api/news/<int:pk>/', NewsApi.as_view({'delete': 'destroy'}), name='destroy-news'),

]
