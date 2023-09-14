from rest_framework import serializers
from .models import *


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ["id" , "image" , "description"]


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["id" , "image" , "title", "body"]
