from rest_framework import serializers
from Calendar.models import *
from Reservation.serializer import ReservationSerializer


class TimeSerializer(serializers.ModelSerializer):
    reservations = ReservationSerializer(read_only=True, many=True)

    class Meta:
        model = Time
        read_only_fields = ['res_id']
        fields = "__all__"


class DaySerializer(serializers.ModelSerializer):

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
        model_fields = ['price', 'off']
        extra_fields = ['all']
        fields = model_fields + extra_fields


class ChangeDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = ['description', 'holiday']

    def update(self, instance, validated_data):
        instance.holiday = validated_data.get("holiday", instance.holiday)
        instance.description = validated_data.get("description", instance.description)
        instance.save()

        return instance
