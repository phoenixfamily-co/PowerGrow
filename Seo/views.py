from django.http import HttpResponse
from django.template import loader
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from About.models import AboutUs
from Seo.models import News
from Seo.serializer import NewsSerializer


def news_view(request):
    about = AboutUs.objects.values().first()
    news = News.objects.all()
    template = loader.get_template('manager/news.html')
    context = {
        "news": news,
        "about": about,
    }
    return HttpResponse(template.render(context, request))


def admin_news_view(request):
    about = AboutUs.objects.values().first()
    news = News.objects.all().values()
    template = loader.get_template('secretary/news.html')
    context = {
        "news": news,
        "about": about,
    }
    return HttpResponse(template.render(context, request))


@permission_classes([IsAdminUser])
class NewsApi(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
