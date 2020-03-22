import logging

from django.db import DatabaseError, transaction
from django.shortcuts import render
from django.views import View
from rest_framework import generics
from rest_framework import filters
from website_content_extractor.forms import QueueTaskForm
from website_content_extractor.models import QueueTask
from website_content_extractor.pagination import ResultSetPagination
from website_content_extractor.serializers import QueueTaskSerializer

from django_filters.rest_framework import DjangoFilterBackend


logger = logging.getLogger(__name__)


class QueueTaskView(View):

    def get(self, request, *args, **kwargs):
        form = QueueTaskForm()
        context = {'form': form}
        return render(request, 'queue_task_form.html', context)

    def post(self, request, *args, **kwargs):
        form = QueueTaskForm(data=request.POST)
        if form.is_valid():
            get_text = form.cleaned_data['get_text']
            get_image = form.cleaned_data['get_image']
            if get_image or get_text:
                try:
                    with transaction.atomic():
                        QueueTask.objects.create(url=form.cleaned_data['url'],
                                                 get_text=form.cleaned_data['get_text'],
                                                 get_image=form.cleaned_data['get_image'])
                except DatabaseError as e:
                    logger.error(e)
                return render(request, 'queue_task_form.html', {'form': QueueTaskForm(), 'status': 'success'})
            else:
                return render(request, 'queue_task_form.html', {'form': form, 'status': 'warning'})
        return render(request, 'queue_task_form.html', {'form': form})


class QueueTaskList(generics.ListCreateAPIView):
    queryset = QueueTask.objects.all()
    serializer_class = QueueTaskSerializer
    pagination_class = ResultSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ('state', 'get_text', 'get_image')
    search_fields = ['url']
    ordering_fields = ['id', 'created_at', 'updated_at']
    ordering = ['created_at']
