import requests
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from Product.models import Participants
from Product.serializer import ParticipantsSerializer
from Reservation.serializer import ReservationSerializer
from .models import User


class AdminRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('number', 'password', 'name', 'birthdate', 'is_active', 'is_teacher', 'is_superuser',
                  'is_staff', 'created')
        extra_kwargs = {
            'password': {'write_only': True},
            'created' : {'read_only': True}
        }

    def create(self, validated_data):
        created = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            created = request.user

        user = User.objects.create(

            number=validated_data['number'],
            name=validated_data['name'],
            password=make_password(validated_data['password']),
            birthdate=validated_data['birthdate'],
            is_active=validated_data['is_active'],
            is_superuser=validated_data['is_superuser'],
            is_staff=validated_data['is_staff'],
            is_teacher=validated_data['is_teacher'],
            created=created

        )
        phone = validated_data["number"]
        phone.replace("+98", " ")

        user.set_password(validated_data['password'])
        user.save()

        data = {'from': '50004001047208', 'to': validated_data['number'],
                'text': "سلام به باشگاه ورزشی حجاب خوش امدید "
                        "\n"
                        f" نام کاربری : {phone} "
                        "\n"
                        f" پسورد : {validated_data['password']} "
                        f"\n"
                        f"https://powergrow.net/"
                }
        requests.post('https://console.melipayamak.com/api/send/simple/d15bf0639e874ecebb5040b599cb8af6',
                      json=data)

        return user


class SecretaryRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('number', 'password', 'name', 'birthdate', 'is_active', 'is_teacher', 'created')
        extra_kwargs = {
            'password': {'write_only': True},
            'created' : {'read_only': True}
        }

    def create(self, validated_data):
        created = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            created = request.user

        user = User.objects.create(

            number=validated_data['number'],
            name=validated_data['name'],
            password=make_password(validated_data['password']),
            birthdate=validated_data['birthdate'],
            is_active=validated_data['is_active'],
            is_teacher=validated_data['is_teacher'],
            created=created

        )
        phone = validated_data["number"]
        phone.replace("+98", " ")

        user.set_password(validated_data['password'])
        user.save()

        data = {'from': '50004001047208', 'to': validated_data['number'],
                'text': "سلام به باشگاه ورزشی حجاب خوش امدید "
                        "\n"
                        f" نام کاربری : {phone} "
                        "\n"
                        f" پسورد : {validated_data['password']} "
                        f"\n"
                        f"https://powergrow.net/"
                }
        requests.post('https://console.melipayamak.com/api/send/simple/d15bf0639e874ecebb5040b599cb8af6',
                      json=data)

        return user


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('number', 'password', 'name', 'birthdate')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create(

            number=validated_data['number'],
            name=validated_data['name'],
            password=make_password(validated_data['password']),
            birthdate=validated_data['birthdate'],

        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['password']

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class ChangeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name']

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()

        return instance


class ChangeNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['number']

    def update(self, instance, validated_data):
        instance.number = validated_data.get("number", instance.number)
        instance.save()

        return instance


class ChangeBirthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['birthdate']

    def update(self, instance, validated_data):
        instance.birthdate = validated_data.get("birthdate", instance.birthdate)
        instance.save()

        return instance


class ChangeSalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['salary', 'fee']

    def update(self, instance, validated_data):
        instance.salary = validated_data.get("salary", instance.salary)
        instance.fee = validated_data.get("fee", instance.fee)
        instance.save()

        return instance


class ChangeDebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['situation', 'debt']

    def update(self, instance, validated_data):
        instance.situation = validated_data.get("situation", instance.situation)
        instance.debt = validated_data.get("debt", instance.debt)
        instance.save()

        return instance


class ChangeDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['description']

    def update(self, instance, validated_data):
        instance.description = validated_data.get("description", instance.description)
        instance.save()

        return instance


class UpdateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['name', 'number', 'birthdate', 'password']

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.number = validated_data.get("number", instance.number)
        instance.birthdate = validated_data.get("birthdate", instance.birthdate)
        instance.set_password(validated_data['password'])

        instance.save()
        return instance


class DeleteAccountSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(required=True)

    class Meta:
        model = User
        fields = ['is_active']

    def update(self, instance, validated_data):
        instance.is_staff = validated_data.get("is_staff", False)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.is_teacher = validated_data.get("is_teacher", False)
        instance.is_superuser = validated_data.get("is_superuser", False)
        instance.save()

        return instance


class GetAccountSerializer(serializers.ModelSerializer):
    reservations = ReservationSerializer(read_only=True, many=True)
    participants = ParticipantsSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = "__all__"


class ManagePermissionSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(required=True)
    is_active = serializers.BooleanField(required=True)
    is_teacher = serializers.BooleanField(required=True)
    is_superuser = serializers.BooleanField(required=True)

    class Meta:
        model = User
        fields = ['is_staff', 'is_active', 'is_teacher', 'is_superuser']

    def update(self, instance, validated_data):
        instance.is_staff = validated_data.get("is_staff", instance.is_staff)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.is_teacher = validated_data.get("is_teacher", instance.is_teacher)
        instance.is_superuser = validated_data.get("is_superuser", instance.is_superuser)
        instance.save()

        return instance


class ManageAccessSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(required=True)
    is_teacher = serializers.BooleanField(required=True)

    class Meta:
        model = User
        fields = ['is_active', 'is_teacher']

    def update(self, instance, validated_data):
        instance.is_staff = validated_data.get("is_staff", False)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.is_teacher = validated_data.get("is_teacher", instance.is_teacher)
        instance.is_superuser = validated_data.get("is_superuser", False)
        instance.save()

        return instance
