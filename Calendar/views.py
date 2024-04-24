from django.http import HttpResponse
from django.template import loader
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from User.models import *
from About.models import AboutUs
from Calendar.serializer import *


def price_view(request):
    about = AboutUs.objects.values().first()
    time = Time.objects.all()
    template = loader.get_template('manager/price.html')
    context = {
        "time": time,
        "about": about,
    }
    return HttpResponse(template.render(context, request))


def calendar_view(request):
    about = AboutUs.objects.values().first()
    day = Day.objects.all()
    template = loader.get_template('manager/calendar.html')
    context = {
        "day": day,
        "about": about,
    }
    return HttpResponse(template.render(context, request))


def teacher_calendar_view(request, pk):
    about = AboutUs.objects.values().first()
    user = User.objects.get(id=pk)
    template = loader.get_template('teacher/calendar.html')
    context = {
        "about": about,
        "user": user,
    }
    return HttpResponse(template.render(context, request))


class YearView(viewsets.ModelViewSet):
    queryset = Year.objects.all()
    serializer_class = YearSerializer

    def get_queryset(self):
        query_set = Year.objects.filter(number=self.kwargs.get('year'))
        return query_set


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


class DayView(viewsets.ModelViewSet):
    queryset = Day.objects.all()
    serializer_class = DaySerializer

    def perform_create(self, serializer):
        data = self.request.data

        Day.objects.update_or_create(
            number=data["number"],
            name=data["name"],
            description=data["description"],
            holiday=bool(self.request.POST.get('reserved', False)),
            month=data["month"],

        )

        times = list([
            "06:30:00", "08:00:00", "09:30:00", "11:00:00", "12:30:00", "14:00:00", "15:30:00", "17:00:00", "18:30:00",
            "20:00:00", "21:30:00", "23:00:00", "00:30:00"])

        for x in range(len(times)):
            Time.objects.update_or_create(
                time=times[x],
                duration=90,
                day=self.get_object().id
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


class ChangeDescriptionView(generics.UpdateAPIView, ):
    queryset = Day.objects.all()
    lookup_field = "id"
    serializer_class = ChangeDescriptionSerializer


class Reset(viewsets.ModelViewSet):
    queryset = Time.objects.all()
    serializer_class = TimeSerializer

    def update(self, request, *args, **kwargs):
        Time.objects.all().update(reserved=False)

        return Response(status=status.HTTP_202_ACCEPTED)
