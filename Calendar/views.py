from rest_framework import viewsets, generics
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

    def get_queryset(self):
        query_set = Time.objects.filter(day=self.kwargs.get('pk')).order_by("time")
        return query_set


class CostView(generics.UpdateAPIView):
    queryset = Time.objects.all()
    serializer_class = ChangeCostSerializer
    lookup_field = "id"
