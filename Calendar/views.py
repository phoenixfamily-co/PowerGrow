from django.http import HttpResponse
from django.template import loader
from rest_framework import viewsets, generics, status
from rest_framework.response import Response

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


class YearView(viewsets.ModelViewSet):
    queryset = Year.objects.all()
    serializer_class = YearSerializer


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


class CostView(generics.UpdateAPIView):
    queryset = Time.objects.all()
    serializer_class = ChangeCostSerializer
    lookup_field = "id"


class ChangeDescriptionView(generics.UpdateAPIView, ):
    queryset = Day.objects.all()
    lookup_field = "id"
    serializer_class = ChangeDescriptionSerializer
