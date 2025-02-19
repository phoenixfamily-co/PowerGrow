from django.urls import path

from Calendar.views import *
from django.conf.urls.static import static
from django.conf import settings


app_name = 'calendar'

urlpatterns = [
    path('price/', price_view, name='price'),
    path('calendar/', calendar_view, name='calendar'),
    path('teacher/<int:pk>/', teacher_calendar_view, name='teacher_calendar'),
    path('user/<int:pk>/', user_calendar_view, name='user_calendar'),
    path('api/year/<int:year>/', YearView.as_view({'post': 'create', 'get': 'list'}), name='year'),
    path('api/month/', MonthView.as_view({'post': 'create', 'get': 'list'}), name='month'),
    path('api/day/', DayView.as_view({'get': 'list'}), name='day'),
    path('api/day/create/', DayView.as_view({'post': 'create'}), name='create_day'),
    path('api/day/<int:pk>/delete/', DayView.as_view({'delete': 'destroy'}), name='day_delete'),
    path('api/time/create/', TimeView.as_view({'post': 'create'}), name='create_time'),
    path('api/time/<int:pk>/', TimeView.as_view({'get': 'list'}), name='get_time'),
    path('api/time/<int:pk>/delete/', TimeView.as_view({'delete': 'destroy'}), name='time_delete'),
    path('api/time/<int:pk>/update/', TimeView.as_view({'put': 'update'}), name='time_update'),
    path('api/cost/<int:id>/', CostView.as_view({'put': 'update'}), name='cost'),
    path('api/description/<int:id>/', ChangeDescriptionView.as_view(), name='description'),
    path('api/time/reset/', Reset.as_view({'put': 'update'}), name='reset'),

    path('api/generate-calendar/', GenerateCalendarAPIView.as_view(), name='generate_calendar'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
