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


class ChangeUserAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('is_staff', 'is_superuser', 'is_teacher', 'is_active')  # می‌توانید فیلدهای دلخواه را اضافه کنید

    def update(self, instance, validated_data):
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        instance.is_teacher = validated_data.get('is_teacher', instance.is_teacher)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

