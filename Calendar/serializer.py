from rest_framework import serializers
from Calendar.models import *


class TimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Time
        read_only_fields = ['daty']
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
    class Meta:
        model = Time
        fields = ['price' , 'off']

    def update(self, instance, validated_data):
        instance.price = validated_data.get("price", instance.price)
        instance.off = validated_data.get("off", instance.off)
        instance.save()

        return instance
