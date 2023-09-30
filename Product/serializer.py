from rest_framework import serializers

from User.serializer import GetAccountSerializer
from .models import Course, Days, Sport, Sessions, Participants


class DaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Days
        fields = "__all__"


class SessionSerializer(serializers.ModelSerializer):
    days = DaysSerializer(read_only=True, many=True)

    class Meta:
        model = Sessions
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    sessions = SessionSerializer(read_only=True, many=True)

    class Meta:
        model = Course
        exclude = ['datetime']


class ParticipantsSerializer(serializers.ModelSerializer):
    user = GetAccountSerializer(read_only=True, many=True)
    course = CourseSerializer(read_only=True, many=True)

    class Meta:
        model = Participants
        fields = "__all__"


class SportSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(read_only=True, many=True)

    class Meta:
        model = Sport
        fields = "__all__"
