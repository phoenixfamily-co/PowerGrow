from django.http import HttpResponse
from django.template import loader
from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from About.models import AboutUs
from Calendar.serializer import *


def calendar_view(request):
    about = AboutUs.objects.values().first()
    time = Time.objects.all()
    template = loader.get_template('manager/price.html')
    context = {
        "time": time,
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

    def perform_create(self, serializer):
        data = self.request.data
        month = Month.objects.get(id=data["month"])
        day = Day.objects.update_or_create(
            name=data["name"],
            number=data["number"],
            description=data["description"],
            holiday=data["holiday"],
            month=month
        )
        serializer = MonthSerializer(day)
        return Response(serializer.data)


class TimeView(viewsets.ModelViewSet):
    queryset = Time.objects.all()
    serializer_class = TimeSerializer

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
