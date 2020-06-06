from rest_framework import serializers

from website_content_extractor.models import WebsiteText, WebsiteImage, QueueTask


class WebsiteTextSerializer(serializers.ModelSerializer):
    task_url = serializers.CharField(source='task.url', read_only=True)

    class Meta:
        model = WebsiteText
        fields = ['id', 'created_at', 'updated_at', 'text', 'task', 'task_url']


class WebsiteImageSerializer(serializers.ModelSerializer):
    task_url = serializers.CharField(source='task.url', read_only=True)

    class Meta:
        model = WebsiteImage
        fields = ['id', 'created_at', 'updated_at', 'image', 'image_url', 'task', 'task_url']


class QueueTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueueTask
        fields = serializers.ALL_FIELDS

    def create(self, validated_data):
        validated_data['state'] = QueueTask.TaskState.PENDING.value
        return QueueTask.objects.create(**validated_data)

    def validate(self, data):
        if not any([data['get_text'], data['get_image']]):
            raise serializers.ValidationError("Both parameters get_text and get_image are set to false")
        return data
