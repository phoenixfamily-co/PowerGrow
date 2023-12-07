from django.urls import path
from Seo.views import *


app_name = 'seo'

urlpatterns = [

    path('news/', news_view, name='news_view'),
    path('api/news/create/', NewsApi.as_view({'post': 'create'}), name='create_news'),
    path('api/news/', NewsApi.as_view({'get': 'list'}), name='news'),
    path('api/news/<int:pk>/', NewsApi.as_view({'delete': 'destroy'}), name='destroy-news'),

]
