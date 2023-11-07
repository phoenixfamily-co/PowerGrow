from rest_framework import serializers
from .models import Course, Days, Sport, Sessions, Participants


class ParticipantsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participants
        read_only_fields = ['created']
        exclude = ['datetime']


class ParticipantsUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participants
        fields = ['user.name']


class DaysSerializer(serializers.ModelSerializer):
    participants = ParticipantsSerializer(read_only=True, many=True)

    class Meta:
        model = Days
        fields = "__all__"


class SessionSerializer(serializers.ModelSerializer):
    days = DaysSerializer(read_only=True, many=True)
    participants = ParticipantsSerializer(read_only=True, many=True)

    class Meta:
        model = Sessions
        fields = "__all__"


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
