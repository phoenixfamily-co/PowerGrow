from django.urls import path

from Calendar.views import *
from django.conf.urls.static import static
from django.conf import settings


app_name = 'calendar'

urlpatterns = [
    path('api/year/', YearView.as_view({'post': 'create', 'get': 'list'}), name='year'),
    path('api/month/', MonthView.as_view({'post': 'create', 'get': 'list'}), name='month'),
    path('api/day/', DayView.as_view({'post': 'create', 'get': 'list'}), name='day'),
    path('api/time/', TimeView.as_view({'post': 'create'}), name='time'),
    path('api/time/<int:pk>/', TimeView.as_view({'get': 'list'}), name='time'),
    path('api/cost/<int:id>/', CostView.as_view(), name='cost'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
