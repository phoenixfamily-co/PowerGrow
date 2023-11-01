from rest_framework import serializers
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


class ParticipantsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participants
        read_only_fields = ['created']
        exclude = ['datetime']
        depth = 1


class CourseSerializer(serializers.ModelSerializer):
    sessions = SessionSerializer(read_only=True, many=True)
    participants = ParticipantsSerializer(read_only=True, many=True)

    class Meta:
        model = Course
        exclude = ['datetime']


class SportSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(read_only=True, many=True)

    class Meta:
        model = Sport
        fields = "__all__"
