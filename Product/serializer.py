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

    def create(self, validated_data):

        user_data = validated_data.pop('user')
        course_data = validated_data.pop('course')
        user = GetAccountSerializer.create(GetAccountSerializer(), validated_data=user_data)
        course = CourseSerializer.create(CourseSerializer(), validated_data=course_data)
        participate, created = Participants.objects.update_or_create(
            user=user,
            title=validated_data.pop('title'),
            session=validated_data.pop('session'),
            day=validated_data.pop('day'),
            price=validated_data.pop('price'),
            course=course

            )
        return participate


class SportSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(read_only=True, many=True)

    class Meta:
        model = Sport
        fields = "__all__"
