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

        if 'password' in validated_data:
            instance.password = make_password(validated_data['password'])

        instance.save()
        return instance
