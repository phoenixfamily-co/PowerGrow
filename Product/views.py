from django.http import HttpResponse
from django.template import loader
from rest_framework import viewsets, filters
from About.models import AboutUs
from Product.serializer import *


def product_view(request, pk, session, day):
    about = AboutUs.objects.values().first()
    product = Course.objects.filter(id=pk).values().first()
    sessions = Sessions.objects.filter(id=session).values().first()
    days = Days.objects.filter(id=day).values().first()
    template = loader.get_template('public/product.html')
    context = {
        "about": about,
        "product": product,
        "session": sessions,
        "days": days,

    }
    return HttpResponse(template.render(context, request))


def payment_view(request, pk, session, day):
    product = Course.objects.filter(id=pk).values().first()
    sessions = Sessions.objects.filter(id=session).values().first()
    days = Days.objects.filter(id=day).values().first()
    template = loader.get_template('public/payment.html')
    context = {
        "product": product,
        "session": sessions,
        "days": days,
    }
    return HttpResponse(template.render(context, request))


def check_view(request, pk, session, day):
    product = Course.objects.filter(id=pk).values().first()
    sessions = Sessions.objects.filter(id=session).values().first()
    days = Days.objects.filter(id=day).values().first()
    template = loader.get_template('public/check.html')
    context = {
        "product": product,
        "session": sessions,
        "days": days,

    }
    return HttpResponse(template.render(context, request))


def sport_view(request, pk):
    template = loader.get_template('public/category.html')
    about = AboutUs.objects.values().first()
    sport = Sport.objects.all().values()
    if not sport.exists():
        return HttpResponse(template.render({}, request))
    else:
        title = Sport.objects.get(id=pk).title
    context = {
        "about": about,
        "title": title,
        "sport": sport,
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

    def get_queryset(self):
        queryset = Days.objects.filter(day=self.kwargs.get('pk'))
        return queryset


class SessionView(viewsets.ModelViewSet):
    serializer_class = SessionSerializer

    def get_queryset(self):
        queryset = Sessions.objects.filter(course=self.kwargs.get('pk'))
        return queryset


class ParticipationView(viewsets.ModelViewSet):
    queryset = Participants.objects.all()
    serializer_class = ParticipantsSerializer


class SportView(viewsets.ModelViewSet):
    queryset = Sport.objects.all()
    serializer_class = SportSerializer
