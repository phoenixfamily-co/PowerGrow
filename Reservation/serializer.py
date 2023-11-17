from rest_framework import serializers

from Reservation.models import *


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservations
        read_only_fields = ['created', 'contract']
        exclude = ['datetime']


class AdminReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservations
        read_only_fields = ['created', 'contract', 'time']
        exclude = ['datetime']


class GymSerializer(serializers.ModelSerializer):
    reservations = ReservationSerializer(read_only=True, many=True)

    class Meta:
        model = Gym
        exclude = ['datetime']
