from django.http import HttpResponse
from django.template import loader
from flask import Response
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from About.models import AboutUs
from Calendar.models import Day
from PowerGrow.decorators import session_auth_required
from Product.models import Course
from Seo.models import News
from Seo.serializer import NewsSerializer
from PowerGrow.permissions import *


@session_auth_required
def news_view(request):
    about = AboutUs.objects.values().first()
    news = News.objects.all().order_by('-pk')
    template = loader.get_template('manager/news.html')
    context = {
        "news": news,
        "about": about,
    }
    return HttpResponse(template.render(context, request))

@session_auth_required
def admin_news_view(request):
    about = AboutUs.objects.values().first()
    news = News.objects.all().order_by('-pk')
    template = loader.get_template('admin/news.html')
    context = {
        "news": news,
        "about": about,
    }
    return HttpResponse(template.render(context, request))


class NewsApi(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAdminUserOrStaff]

    def perform_create(self, serializer):
        data = self.request.data
        title = data["title"]
        description = data["description"]
        date = Day.objects.filter(id=self.kwargs['day']).first()
        course = Course.objects.filter(id=data["course"]).first()
        news = News.objects.update_or_create(title=title, description=description, date=date, course=course)

        serializer = NewsSerializer(news)
        return Response(serializer.data)


