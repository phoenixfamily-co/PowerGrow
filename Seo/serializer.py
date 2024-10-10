from rest_framework import serializers

from Seo.models import News


class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = "__all__"
