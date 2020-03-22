from rest_framework import serializers

from website_content_extractor.models import WebsiteText, WebsiteImage, QueueTask


class WebsiteTextSerializer(serializers.ModelSerializer):
    task_url = serializers.CharField(source='task.url', read_only=True)

    class Meta:
        model = WebsiteText
        fields = ['id', 'created_at', 'updated_at', 'text', 'task', 'task_url']


class WebsiteImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteImage
        fields = serializers.ALL_FIELDS


class QueueTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueueTask
        fields = serializers.ALL_FIELDS
