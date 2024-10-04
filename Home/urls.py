from django.urls import path
from Home.views import *
from django.conf.urls.static import static
from django.conf import settings


app_name = 'home'

urlpatterns = [
    path('', home_view, name='home'),
    path('slider/', slider_view, name='slider_view'),
    path('api/slider/create/', SliderView.as_view({'post': 'create'}), name='create_slider'),
    path('api/slider/update/<int:pk>/', SliderView.as_view({'put': 'update'}), name='update_slider'),
    path('api/slider/', SliderView.as_view({'get': 'list'}), name='slider'),
    path('api/slider/<int:pk>/', SliderView.as_view({'delete': 'destroy'}), name='delete-slider')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
