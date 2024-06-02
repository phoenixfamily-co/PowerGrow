from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, generics, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from User.models import *
from Product.models import *
from Reservation.models import *
from About.models import AboutUs
from Calendar.serializer import *


def price_view(request):
    about = AboutUs.objects.values().first()
    time = Time.objects.all().order_by('-day_id', 'pk')
    template = loader.get_template('manager/price.html')
    p = Paginator(time, 50)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)

    context = {
        'page_obj': page_obj,
        "about": about,
    }
    return HttpResponse(template.render(context, request))


def calendar_view(request):
    about = AboutUs.objects.values().first()
    day = Day.objects.all().order_by('-pk')
    template = loader.get_template('manager/calendar.html')
    p = Paginator(day, 50)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)

    context = {
        'page_obj': page_obj,
        "about": about,
    }
    return HttpResponse(template.render(context, request))


def teacher_calendar_view(request, pk):
    about = AboutUs.objects.values().first()
    user = User.objects.get(id=pk)
    participants = Participants.objects.filter(user_id=pk)
    thisList = []

    for x in participants:
        week = Days.objects.filter(id=x.day.id).first()
        day = week.title.split("،")
        ids = Day.objects.filter(name__in=day, month__number__gte=x.startDay.month.number,
                                 month__year__number__gte=x.startDay.month.year.number, holiday=False).exclude(
            month__number=x.startDay.month.number,
            number__lt=x.startDay.number) \
                  .order_by('pk').values_list('pk', flat=True)[:int(x.session.number)]
        thisList.extend(list(ids))

    template = loader.get_template('teacher/calendar.html')

    context = {
        "about": about,
        "user": user,
        "participants": participants,
        "thisList": thisList,

    }
    return HttpResponse(template.render(context, request))


def user_calendar_view(request, pk):
    about = AboutUs.objects.values().first()
    user = User.objects.get(id=pk)
    participants = Participants.objects.filter(user_id=pk)
    reservation = Reservations.objects.filter(user_id=pk)

    thisList = []

    resList = []

    for x in participants:
        week = Days.objects.filter(id=x.day.id).first()
        day = week.title.split("،")
        ids = Day.objects.filter(name__in=day, month__number__gte=x.startDay.month.number,
                                 month__year__number__gte=x.startDay.month.year.number, holiday=False).exclude(
            month__number=x.startDay.month.number,
            number__lt=x.startDay.number) \
                  .order_by('pk').values_list('pk', flat=True)[:int(x.session.number)]
        thisList.extend(list(ids))

    for x in reservation:
        if x.holiday:
            ids = Day.objects.filter(name=x.time.day.name,
                                     month__number__gte=x.time.day.month.number) \
                      .exclude(month__number=x.time.day.month.number,
                               number__lt=x.time.day.number).exclude(
                holiday=x.holiday) \
                      .order_by('month__number').values_list('pk', flat=True)[:int(x.session)]
        else:
            ids = Day.objects.filter(name=x.time.day.name, time=x.time.time,
                                     month__number__gte=x.time.day.month.number) \
                      .exclude(month__number=x.time.day.month.number,
                               number__lt=x.time.day.number) \
                      .order_by('month__number').values_list('pk', flat=True)[:int(x.session)]

        resList.extend(list(ids))

    template = loader.get_template('teacher/calendar.html')

    context = {
        "about": about,
        "user": user,
        "participants": participants,
        "thisList": thisList,
        "resList": resList,
        "reservation": reservation,

    }
    return HttpResponse(template.render(context, request))


class YearView(viewsets.ModelViewSet):
    queryset = Year.objects.all()
    serializer_class = YearSerializer

    def get_queryset(self):
        query_set = Year.objects.filter(number=self.kwargs.get('year'))
        return query_set


@permission_classes([IsAuthenticated])
class MonthView(viewsets.ModelViewSet):
    queryset = Month.objects.all()
    serializer_class = MonthSerializer

    def perform_create(self, serializer):
        data = self.request.data
        year = Year.objects.get(id=data["year"])
        month = Month.objects.update_or_create(
            name=data["name"],
            number=data["number"],
            max=data["max"],
            year=year
        )
        serializer = MonthSerializer(month)
        return Response(serializer.data)


@permission_classes([IsAuthenticated])
class DayView(viewsets.ModelViewSet):
    queryset = Day.objects.all()
    serializer_class = DaySerializer

    def perform_create(self, serializer):
        data = self.request.data

        day = Day.objects.create(
            number=data["number"],
            name=data["name"],
            description=data["description"],
            holiday=bool(self.request.POST.get('holiday', False)),
            month_id=data["month"],
        )

        day.save()

        times = list([
            "06:30:00", "08:00:00", "09:30:00", "11:00:00", "12:30:00", "14:00:00", "15:30:00", "17:00:00", "18:30:00",
            "20:00:00", "21:30:00", "23:00:00", "00:30:00"])

        for x in range(len(times)):
            Time.objects.update_or_create(
                time=times[x],
                duration=90,
                day_id=day.id
            )


class TimeView(viewsets.ModelViewSet):
    queryset = Time.objects.all()
    serializer_class = TimeSerializer

    def perform_create(self, serializer):
        data = self.request.data
        day = Day.objects.get(id=self.kwargs["pk"])
        time = Time.objects.update_or_create(
            time=data["time"],
            duration=data["duration"],
            reserved=bool(self.request.POST.get('reserved', False)),
            price=data["price"],
            off=data["off"],
            day=day

        )
        serializer = TimeSerializer(time)
        return Response(serializer.data)

    def get_queryset(self):
        query_set = Time.objects.filter(day=self.kwargs.get('pk')).order_by("time")
        return query_set

    def destroy(self, request, *args, **kwargs):
        queryset = Time.objects.get(id=kwargs.get('pk'))
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes([IsAdminUser])
class CostView(viewsets.ModelViewSet):
    queryset = Time.objects.all()
    serializer_class = ChangeCostSerializer

    def update(self, request, *args, **kwargs):
        time = Time.objects.get(id=kwargs.get('id'))
        is_all = bool(self.request.POST.get("all"))
        if is_all:
            Time.objects.filter(time=time.time, day__name=time.day.name).update(price=request.data['price'])
        else:
            Time.objects.filter(id=kwargs.get('id')).update(price=request.data['price'])

        return Response(status=status.HTTP_202_ACCEPTED)


@permission_classes([IsAdminUser])
class ChangeDescriptionView(generics.UpdateAPIView, ):
    queryset = Day.objects.all()
    lookup_field = "id"
    serializer_class = ChangeDescriptionSerializer


@permission_classes([IsAdminUser])
class Reset(viewsets.ModelViewSet):
    queryset = Time.objects.all()
    serializer_class = TimeSerializer

    def update(self, request, *args, **kwargs):
        Time.objects.all().update(reserved=False)

        return Response(status=status.HTTP_202_ACCEPTED)
