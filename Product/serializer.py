from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "image", "title", "name", "day", "type", "time", "session", "tuition" , "description"
            , "selected", "capacity", "gender", "start"]
