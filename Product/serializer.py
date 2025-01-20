from rest_framework import serializers

from .models import Course, Days, Sport, Session, Participants, Offers


class ManagerParticipantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participants
        fields = [
            'id',  # شناسه
            'description',  # توضیحات
            'session',  # جلسه
            'day',  # روز
            'startDay',  # روز شروع
            'endDay',  # روز پایان
            'price',  # قیمت
            'user',  # کاربر
            'course',  # دوره
            'success',  # وضعیت موفقیت
            'created',
        ]

    def create(self, validated_data):
        return Participants.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.session = validated_data.get('session', instance.session)
        instance.day = validated_data.get('day', instance.day)
        instance.startDay = validated_data.get('startDay', instance.startDay)
        instance.endDay = validated_data.get('endDay', instance.endDay)
        instance.price = validated_data.get('price', instance.price)
        instance.course = validated_data.get('course', instance.course)
        instance.user = validated_data.get('user', instance.user)

        instance.save()
        return instance


class ParticipantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participants
        fields = ['description', 'startDay', 'endDay', 'session', 'day', 'price', 'user', 'course',
                  'authority', 'success']

    def create(self, validated_data):
        return Participants.objects.create(**validated_data)


class DaysCreateSerializer(serializers.ModelSerializer):
    participants = ParticipantsSerializer(read_only=True, many=True)

    class Meta:
        model = Days
        fields = "__all__"

    def create(self, validated_data):
        return Days.objects.create(**validated_data)


class DaysSerializer(serializers.ModelSerializer):
    participants = ParticipantsSerializer(read_only=True, many=True)

    class Meta:
        model = Days
        fields = "__all__"
        read_only_fields = ('tuition', 'off')

    def create(self, validated_data):
        return Days.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.session = validated_data.get('session', instance.session)
        instance.save()
        return instance


class SessionSerializer(serializers.ModelSerializer):
    days = DaysSerializer(read_only=True, many=True)
    participants = ParticipantsSerializer(read_only=True, many=True)

    class Meta:
        model = Session
        fields = "__all__"

    def create(self, validated_data):
        return Session.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.number = validated_data.get('number', instance.number)
        instance.active = validated_data.get('active', instance.active)
        instance.course = validated_data.get('course', instance.course)
        instance.save()
        return instance


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = ['datetime']

    def create(self, validated_data):
        return Course.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.name = validated_data.get('name', instance.name)
        instance.type = validated_data.get('type', instance.type)
        instance.description = validated_data.get('description', instance.description)
        instance.time = validated_data.get('time', instance.time)
        instance.selected = validated_data.get('selected', instance.selected)
        instance.capacity = validated_data.get('capacity', instance.capacity)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.sport = validated_data.get('sport', instance.sport)
        instance.active = validated_data.get('active', instance.active)

        instance.save()
        return instance


class SportSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(read_only=True, many=True)

    class Meta:
        model = Sport
        fields = "__all__"

    def create(self, validated_data):
        return Sport.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance


class ChangeDayPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Days
        fields = ('tuition', 'off')  # می‌توانید فیلدهای دلخواه را اضافه کنید

    def update(self, instance, validated_data):
        instance.tuition = validated_data.get('tuition', instance.tuition)
        instance.off = validated_data.get('off', instance.off)
        instance.save()
        return instance


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offers
        fields = [
            'id',  # شناسه
            'type',  # توضیحات
            'product',  # جلسه
            'session',  # روز
            'off',  # روز شروع
        ]

    def create(self, validated_data):
        return Offers.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.type = validated_data.get('type', instance.type)
        instance.product = validated_data.get('product', instance.product)
        instance.session = validated_data.get('session', instance.session)
        instance.off = validated_data.get('off', instance.off)

        instance.save()
        return instance


class UpdateDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Participants
        fields = ['startDay', 'endDay']

    def validate(self, attrs):
        start_day = attrs.get('startDay')
        end_day = attrs.get('endDay')

        return attrs

    def update(self, instance, validated_data):
        instance.startDay = validated_data.get('startDay', instance.startDay)
        instance.endDay = validated_data.get('endDay', instance.endDay)
        instance.save()

        return instance
