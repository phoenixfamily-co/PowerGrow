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


class ManagerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'birthdate', 'description')  # می‌توانید فیلدهای دلخواه را اضافه کنید

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.birthdate = validated_data.get('birthdate', instance.birthdate)
        instance.description = validated_data.get('description', instance.description)

        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'birthdate', 'email')  # می‌توانید فیلدهای دلخواه را اضافه کنید

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.birthdate = validated_data.get('birthdate', instance.birthdate)
        instance.email = validated_data.get('email', instance.description)

        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)


class ChangeNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['number']

    def update(self, instance, validated_data):
        instance.number = validated_data.get('number', instance.number)
        instance.save()
        return instance


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


class ChangeUserSalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('salary', 'fee', 'situation', 'debt')  # می‌توانید فیلدهای دلخواه را اضافه کنید

    def update(self, instance, validated_data):
        instance.salary = validated_data.get('salary', instance.salary)
        instance.fee = validated_data.get('fee', instance.fee)
        instance.situation = validated_data.get('situation', instance.situation)
        instance.debt = validated_data.get('debt', instance.debt)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # یا می‌توانید فیلدهای خاصی را تعیین کنید