from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('number', 'password', 'gender', 'name')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            number=validated_data['number'],
            name=validated_data['name'],
            gender=validated_data['gender'],
            password=make_password(validated_data['password']),

        )
        user.set_password(validated_data['password'])
        user.save()

        return user
