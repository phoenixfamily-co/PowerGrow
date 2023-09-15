from rest_framework import serializers
from .models import *


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = ["id" , "telegram" , "instagram", "telephone", "phone", "logo", "address",
                  "transparent_logo", "latitude", "longitude"]
