from django.http import HttpResponse
from django.template import loader
from rest_framework import viewsets, filters
from About.models import AboutUs
from Product.models import *
from Product.serializer import *


def product_view(request, pk, session, day):
    about = AboutUs.objects.values().first()
    product = Course.objects.filter(id=pk).values().first()
    course = Course.objects.get()
    days = course.days.get(id=day, course=pk)
    template = loader.get_template('public/product.html')
    context = {
        "instagram": about["instagram"],
        "telegram": about["telegram"],
        "telephone": about["telephone"],
        "phone": about["phone"],
        "logo": about["logo"],
        "transparent_logo": about["transparent_logo"],
        "address": about["address"],
        "latitude": about["latitude"],
        "longitude": about["longitude"],
        "title": product["title"],
        "name": product["name"],
        "days": days,
        "type": product["type"],
        "time": product["time"],
        "session": session,
        "tuition": product["tuition"],
        "off": product["off"],
        "price": product["price"],
        "description": product["description"],
        "start": product["start"],
        "image": product["image"],
        "profile": product["profile"],
        "selected": product["selected"],
        "capacity": product["capacity"],
        "gender": product["gender"],
        "datetime": product["datetime"],
    }
    return HttpResponse(template.render(context, request))


def sport_view(request, pk):
    about = AboutUs.objects.values().first()
    category = Sport.objects.all().values()
    sport = Sport.objects.get(id=pk)
    template = loader.get_template('public/category.html')
    context = {
        "instagram": about["instagram"],
        "telegram": about["telegram"],
        "telephone": about["telephone"],
        "phone": about["phone"],
        "logo": about["logo"],
        "transparent_logo": about["transparent_logo"],
        "address": about["address"],
        "latitude": about["latitude"],
        "longitude": about["longitude"],
        "sport": sport.course,
        "title": sport.title,
        "category": category,
        "id": pk
    }
    return HttpResponse(template.render(context, request))


class CourseView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [filters.SearchFilter]


class SearchView(viewsets.generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'title']

    def get_queryset(self):
        return Course.objects.filter(sport=self.kwargs['pk'])


class DaysView(viewsets.ModelViewSet):
    queryset = Days.objects.all()
    serializer_class = DaysSerializer


class SessionView(viewsets.ModelViewSet):
    queryset = Sessions.objects.all()
    serializer_class = SessionSerializer


class ParticipationView(viewsets.ModelViewSet):
    queryset = Participants.objects.all()
    serializer_class = ParticipantsSerializer


class SportView(viewsets.ModelViewSet):
    queryset = Sport.objects.all()
    serializer_class = SportSerializer
