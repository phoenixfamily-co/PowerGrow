from rest_framework import serializers
from .models import *


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        exclude = ['datetime']
