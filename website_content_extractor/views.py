from django.shortcuts import render
from django.views import View
from django.views.generic import FormView

from website_content_extractor.forms import QueueTaskForm


class QueueTaskView(FormView):
    template_name = 'queue_task_form.html'
    form_class = QueueTaskForm
    success_url = '/'
