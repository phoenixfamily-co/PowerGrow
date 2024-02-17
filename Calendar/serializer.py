from rest_framework import serializers
from Calendar.models import *


class TimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Time
        read_only_fields = ['day']
        fields = "__all__"


class DaySerializer(serializers.ModelSerializer):
    times = TimeSerializer(read_only=True, many=True)

    class Meta:
        model = Day
        fields = "__all__"


class MonthSerializer(serializers.ModelSerializer):
    days = DaySerializer(read_only=True, many=True)

    class Meta:
        model = Month
        fields = "__all__"


class YearSerializer(serializers.ModelSerializer):
    months = MonthSerializer(read_only=True, many=True)

    class Meta:
        model = Year
        fields = "__all__"


class ChangeCostSerializer(serializers.ModelSerializer):
    all = serializers.BooleanField()

    class Meta:
        model = Time
        fields = ['price', 'off']
        read_only_fields = ('all',)


class ChangeDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = ['description', 'holiday']

    def update(self, instance, validated_data):
        instance.holiday = validated_data.get("holiday", instance.holiday)
        instance.description = validated_data.get("description", instance.description)
        instance.save()

        return instance

