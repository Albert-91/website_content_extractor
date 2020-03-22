from rest_framework import serializers

from website_content_extractor.models import WebsiteText, WebsiteImage, QueueTask


class WebsiteTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteText
        fields = serializers.ALL_FIELDS


class WebsiteImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteImage
        fields = serializers.ALL_FIELDS


class QueueTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueueTask
        fields = serializers.ALL_FIELDS
