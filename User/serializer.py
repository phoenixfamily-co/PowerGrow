from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('number', 'password', 'name', 'birthdate')  # می‌توانید فیلدهای دلخواه را اضافه کنید
        extra_kwargs = {
            'password': {'write_only': True}  # رمز عبور فقط برای نوشتن است
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User(**validated_data)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'birthdate')  # می‌توانید فیلدهای دلخواه را اضافه کنید

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.birthdate = validated_data.get('birthdate', instance.birthdate)

        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)


class ChangeUserAccessSerializer(serializers.Serializer):
    is_staff = serializers.BooleanField(required=True)
    is_superuser = serializers.BooleanField(required=True)
    is_teacher = serializers.BooleanField(required=True)
    is_active = serializers.BooleanField(required=True)

