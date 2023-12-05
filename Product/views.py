from django.http import HttpResponse
from django.template import loader
from rest_framework import viewsets, filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from About.models import AboutUs
from User.models import *
from Product.serializer import *


def product_view(request, pk, session, day):
    about = AboutUs.objects.values().first()
    sport = Sport.objects.all().values()
    product = Course.objects.get(id=pk)
    participants = Participants.objects.filter(course__pk=pk).values()
    sessions = Sessions.objects.filter(id=session).values().first()
    days = Days.objects.filter(id=day).values().first()
    template = loader.get_template('public/product.html')
    context = {
        "about": about,
        "product": product,
        "participants": len(list(participants)),
        "session": sessions,
        "sport": sport,
        "days": days,

    }
    return HttpResponse(template.render(context, request))


def payment_view(request, pk, session, day):
    about = AboutUs.objects.values().first()
    product = Course.objects.filter(id=pk).values().first()
    sessions = Sessions.objects.filter(id=session).values().first()
    days = Days.objects.filter(id=day).values().first()
    template = loader.get_template('public/payment.html')
    context = {
        "about": about,
        "product": product,
        "session": sessions,
        "day": days,
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


def category_view(request, pk):
    template = loader.get_template('public/category.html')
    about = AboutUs.objects.values().first()
    sport = Sport.objects.all()
    course = Course.objects.all()
    context = {
        "about": about,
        "sport": sport,
        "selected" : course.filter(sport=pk).values(),
        "title": sport.filter(id=pk).values().first(),
        "id": pk
    }
    return HttpResponse(template.render(context, request))


def sports_view(request):
    template = loader.get_template('manager/sports.html')
    sport = Sport.objects.all()
    about = AboutUs.objects.values().first()
    context = {
        "about": about,
        "sport": sport,
    }
    return HttpResponse(template.render(context, request))


def courses_view(request):
    template = loader.get_template('manager/courses.html')
    course = Course.objects.all()
    about = AboutUs.objects.values().first()
    context = {
        "about": about,
        "course": course,
    }
    return HttpResponse(template.render(context, request))


def session_view(request):
    template = loader.get_template('manager/sessions.html')
    session = Sessions.objects.all()
    about = AboutUs.objects.values().first()
    context = {
        "about": about,
        "session": session,
    }
    return HttpResponse(template.render(context, request))


def day_view(request):
    template = loader.get_template('manager/days.html')
    day = Days.objects.all()
    about = AboutUs.objects.values().first()
    context = {
        "about": about,
        "day": day,
    }
    return HttpResponse(template.render(context, request))


class CourseView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SearchView(viewsets.generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'title']

    def get_queryset(self):
        return Course.objects.filter(sport=self.kwargs['pk'])


class DaysView(generics.GenericAPIView):
    queryset = Days.objects.all()
    serializer_class = DaysSerializer
    lookup_field = 'course'


class SessionView(generics.GenericAPIView):
    queryset = Sessions.objects.all()
    serializer_class = SessionSerializer
    lookup_field = 'course'


class ParticipationView(viewsets.ModelViewSet):
    queryset = Participants.objects.all()
    serializer_class = ParticipantsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Participants.objects.filter(user=self.request.user.id)
        return queryset

    def perform_create(self, serializer):
        data = self.request.data
        session = Sessions.objects.filter(id=data["session"]).first()
        day = Days.objects.filter(id=data["day"]).first()
        course = Course.objects.filter(id=data["course"]).first()
        participants = Participants.objects.update_or_create(title=data["title"],
                                                             session=session,
                                                             day=day,
                                                             price=data["price"],
                                                             user=self.request.user,
                                                             course=course,
                                                             created=self.request.user)
        serializer = ParticipantsSerializer(participants)
        return Response(serializer.data)


class ManagerParticipationView(viewsets.ModelViewSet):
    queryset = Participants.objects.all()
    serializer_class = ParticipantsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        data = self.request.data
        session = Sessions.objects.filter(id=data["session"]).first()
        day = Days.objects.filter(id=data["day"]).first()
        course = Course.objects.filter(id=self.kwargs['id']).first()
        user = User.objects.filter(id=data["user"]).first()
        participants = Participants.objects.update_or_create(title=data["title"],
                                                             description=data["description"],
                                                             session=session,
                                                             day=day,
                                                             price=data["price"],
                                                             user=user,
                                                             course=course,
                                                             created=self.request.user)
        serializer = ParticipantsSerializer(participants)
        return Response(serializer.data)


class SportView(viewsets.ModelViewSet):
    queryset = Sport.objects.all()
    serializer_class = SportSerializer


class CourseUserView(generics.ListAPIView):
    queryset = Participants.objects.all()
    serializer_class = ParticipantsUserSerializer
    lookup_field = "id"
