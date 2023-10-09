from rest_framework import viewsets
from rest_framework.response import Response

from Calendar.serializer import *


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
    lookup_field = "day"
