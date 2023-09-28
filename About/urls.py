from django.urls import path
from About.views import *


app_name = 'aboutUs'

urlpatterns = [
    path('', about_view, name='aboutUs'),
    path('api/', About.as_view({'post': 'create', 'get': 'list'}), name='about'),

]
