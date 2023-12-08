from django.urls import path

from Calendar.views import *
from django.conf.urls.static import static
from django.conf import settings


app_name = 'calendar'

urlpatterns = [
    path('price/', price_view, name='price'),
    path('calendar/', price_view, name='calendar'),
    path('api/year/', YearView.as_view({'post': 'create', 'get': 'list'}), name='year'),
    path('api/month/', MonthView.as_view({'post': 'create', 'get': 'list'}), name='month'),
    path('api/day/', DayView.as_view({'post': 'create', 'get': 'list'}), name='day'),
    path('api/time/<int:pk>/create/', TimeView.as_view({'post': 'create'}), name='create_time'),
    path('api/time/<int:pk>/', TimeView.as_view({'get': 'list'}), name='get_time'),
    path('api/time/<int:pk>/delete/', TimeView.as_view({'delete': 'destroy'}), name='time_delete'),
    path('api/time/<int:pk>/update/', TimeView.as_view({'put': 'update'}), name='time_update'),
    path('api/cost/<int:id>/', CostView.as_view(), name='cost'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
