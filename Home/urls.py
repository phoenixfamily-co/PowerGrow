from django.urls import path
from Home import views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'home'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('api/slider', views.get_slider, name='home_slider'),
    path('api/upload', views.UploadImage.as_view({'post': 'create'}), name='home_upload'),
    path('api/selected', views.get_selected, name='selected_course')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
