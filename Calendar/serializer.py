from rest_framework import serializers
from Calendar.models import *


class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = "__all__"
        depth = 1


class MonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Month
        fields = "__all__"
        depth = 1


class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = "__all__"
        depth = 2


class TimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time
        fields = "__all__"
