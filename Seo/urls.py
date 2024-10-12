from django.urls import path
from Seo.views import *


app_name = 'seo'

urlpatterns = [

    path('news/manager/', manager_news_view, name='manager_news_view'),
    path('news/admin/', admin_news_view, name='admin_news_view'),
    path('news/teacher/', teacher_news_view, name='teacher_news_view'),
    path('news/user/', user_news_view, name='user_news_view'),

    path('api/news/create/', NewsApi.as_view({'post': 'create'}), name='create_news'),
    path('api/news/', NewsApi.as_view({'get': 'list'}), name='news'),
    path('api/news/delete/<int:pk>/', NewsApi.as_view({'delete': 'destroy'}), name='destroy_news'),
    path('api/news/update/<int:pk>/', NewsApi.as_view({'put': 'update'}), name='update_news'),

]
