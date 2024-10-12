from rest_framework import serializers

from Seo.models import News


class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = "__all__"
        extra_kwargs = {
            'users_who_read': {'read_only': True}  # این فیلد فقط خواندنی است
        }

    def create(self, validated_data):
        return News.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.date = validated_data.get('date', instance.date)
        instance.course = validated_data.get('course', instance.course)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
