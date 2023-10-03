from django.urls import path

from Calendar.views import *
from django.conf.urls.static import static
from django.conf import settings


app_name = 'calendar'

urlpatterns = [
    path('api/year/', YearView.as_view({'post': 'create', 'get': 'list'}), name='calendar'),
    path('api/month/', MonthView.as_view({'post': 'create', 'get': 'list'}), name='calendar'),
    path('api/day/', DayView.as_view({'post': 'create', 'get': 'list'}), name='calendar'),
    path('api/time/', TimeView.as_view({'post': 'create', 'get': 'list'}), name='calendar'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
