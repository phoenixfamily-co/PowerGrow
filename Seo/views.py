from rest_framework import viewsets

from Seo.models import News
from Seo.serializer import NewsSerializer


class newsApi(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
