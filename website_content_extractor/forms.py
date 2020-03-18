from django import forms

from website_content_extractor.models import QueueTask


class QueueTaskForm(forms.ModelForm):

    class Meta:
        model = QueueTask
        fields = ['url', 'get_text', 'get_image']
