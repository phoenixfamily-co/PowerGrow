from rest_framework import serializers

from Reservation.models import *


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservations
        exclude = ['datetime']


class GymSerializer(serializers.ModelSerializer):
    # reservations = ReservationSerializer(read_only=True, many=True)

    class Meta:
        model = Gym
        exclude = ['datetime']
