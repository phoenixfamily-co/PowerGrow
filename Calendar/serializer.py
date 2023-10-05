from rest_framework import serializers
from Calendar.models import *


class TimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Time
        fields = "__all__"


class DaySerializer(serializers.ModelSerializer):
    times = TimeSerializer(read_only=True, many=True)

    class Meta:
        model = Day
        fields = "__all__"
        depth = 2


class MonthSerializer(serializers.ModelSerializer):
    days = DaySerializer(read_only=True, many=True)

    class Meta:
        model = Month
        fields = "__all__"
        depth = 1


class YearSerializer(serializers.ModelSerializer):
    months = MonthSerializer(read_only=True, many=True)

    class Meta:
        model = Year
        fields = "__all__"
        depth = 1



