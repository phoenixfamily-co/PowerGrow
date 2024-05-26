from rest_framework import serializers
from .models import Course, Days, Sport, Sessions, Participants


class ManagerParticipantsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participants
        read_only_fields = ['authority', 'success', 'created', 'course', 'startDay', 'session', 'day', 'endDay', 'user']
        exclude = ['datetime']


class RegisterParticipantsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participants
        read_only_fields = ['authority', 'success', 'created', 'user', 'startDay', 'session', 'day', 'endDay']
        exclude = ['datetime']


class ParticipantsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participants
        read_only_fields = ['created', 'endDay']
        exclude = ['datetime']


class ParticipantsUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participants
        fields = ['user']


class ChangeDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Participants
        fields = ['endDay']

    def update(self, instance, validated_data):
        instance.endDay = validated_data.get("endDay", instance.endDay)
        instance.save()

        return instance


class ChangeDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participants
        fields = ['description']

    def update(self, instance, validated_data):
        instance.description = validated_data.get("description", instance.description)
        instance.save()

        return instance



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
