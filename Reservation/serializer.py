from rest_framework import serializers

from Reservation.models import *


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservations
        read_only_fields = ['created', 'endDate']
        exclude = ['datetime']


class AdminReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservations
        read_only_fields = ['created', 'time', 'authority', 'success', 'endDate', 'user']
        exclude = ['datetime']


class GymSerializer(serializers.ModelSerializer):
    reservations = ReservationSerializer(read_only=True, many=True)

    class Meta:
        model = Gym
        exclude = ['datetime']
