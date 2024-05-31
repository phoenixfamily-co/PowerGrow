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


class UpdateSessionSerializer(serializers.ModelSerializer):
    days = DaysSerializer(read_only=True, many=True)
    participants = ParticipantsSerializer(read_only=True, many=True)

    class Meta:
        model = Sessions
        fields = "number"



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


class ChangeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name']

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()

        return instance


class ChangeTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title']

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.save()

        return instance


class ChangeGenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['gender']

    def update(self, instance, validated_data):
        instance.gender = validated_data.get("gender", instance.gender)
        instance.save()

        return instance


class ChangeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['type']

    def update(self, instance, validated_data):
        instance.type = validated_data.get("type", instance.type)
        instance.save()

        return instance


class ChangeTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['time']

    def update(self, instance, validated_data):
        instance.time = validated_data.get("time", instance.time)
        instance.save()

        return instance


class ChangeSportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['sport']

    def update(self, instance, validated_data):
        instance.sport = validated_data.get("sport", instance.sport)
        instance.save()

        return instance


class ChangeCapacitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['capacity']

    def update(self, instance, validated_data):
        instance.capacity = validated_data.get("capacity", instance.capacity)
        instance.save()

        return instance


class UpdateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['image', 'selected', 'description']

    def update(self, instance, validated_data):
        instance.image = validated_data.get("image", instance.image)
        instance.selected = validated_data.get("selected", instance.selected)
        instance.description = validated_data.get("description", instance.description)

        instance.save()

        return instance


class ChangePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participants
        fields = ['price']

    def update(self, instance, validated_data):
        instance.price = validated_data.get("price", instance.price)
        instance.save()

        return instance


class ChangeCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participants
        fields = ['course']

    def update(self, instance, validated_data):
        instance.course = validated_data.get("course", instance.course)
        instance.save()

        return instance

