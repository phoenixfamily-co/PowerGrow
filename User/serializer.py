from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('number', 'password', 'gender', 'name' , 'birthdate')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            number=validated_data['number'],
            name=validated_data['name'],
            gender=validated_data['gender'],
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


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        extra_kwargs = {
            'number': {'required': False},
            'name': {'required': True},
            'gender': {'required': True},
            'birthdate': {'required': True},
            'password': {'write_only': True}
        }
        exclude = ['number']

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name",  instance.name)
        instance.gender = validated_data.get("gender",  instance.gender)
        instance.national = validated_data.get("national",  instance.national)
        instance.birthdate = validated_data.get("birthdate",  instance.birthdate)
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
        instance.is_admin = validated_data.get("is_admin", False)
        instance.is_superuser = validated_data.get("is_superuser", False)
        instance.save()

        return instance


class GetAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class ManagePermissionSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(required=True)
    is_active = serializers.BooleanField(required=True)
    is_admin = serializers.BooleanField(required=True)
    is_superuser = serializers.BooleanField(required=True)

    class Meta:
        model = User
        fields = ['is_staff', 'is_active', 'is_admin', 'is_superuser']

    def update(self, instance, validated_data):
        instance.is_staff = validated_data.get("is_staff", instance.is_staff)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.is_admin = validated_data.get("is_admin", instance.is_admin)
        instance.is_superuser = validated_data.get("is_superuser", instance.is_superuser)
        instance.save()

        return instance
