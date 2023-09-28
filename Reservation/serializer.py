from rest_framework import serializers

from Reservation.models import *


class TimesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Times
        fields = "__all__"


class DatesSerializer(serializers.ModelSerializer):
    times = TimesSerializer(read_only=True, many=True)

    class Meta:
        model = Dates
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservations
        exclude = ['datetime']


class GymSerializer(serializers.ModelSerializer):
    reservations = ReservationSerializer(read_only=True, many=True)
    dates = DatesSerializer(read_only=True, many=True)

    class Meta:
        model = Gym
        fields = "__all__"
