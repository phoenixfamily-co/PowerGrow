from django.urls import path
from Seo.views import *


app_name = 'seo'

urlpatterns = [

    path('api/news/', NewsApi.as_view({'post': 'create', 'get': 'list'}), name='news'),

]
