import logging
from wsgiref.util import FileWrapper

from django.db import DatabaseError, transaction
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics
from rest_framework.views import APIView

from website_content_extractor.forms import QueueTaskForm
from website_content_extractor.models import QueueTask, WebsiteText, WebsiteImage
from website_content_extractor.pagination import ResultSetPagination
from website_content_extractor.serializers import QueueTaskSerializer, WebsiteTextSerializer, WebsiteImageSerializer

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


class QueueTaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = QueueTask.objects.all()
    serializer_class = QueueTaskSerializer


class WebsiteTextList(generics.ListAPIView):
    queryset = WebsiteText.objects.all()
    serializer_class = WebsiteTextSerializer
    pagination_class = ResultSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['text']
    ordering_fields = ['id', 'created_at', 'updated_at']
    ordering = ['created_at']


class WebsiteTextDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = WebsiteText.objects.all()
    serializer_class = WebsiteTextSerializer


class WebsiteImageList(generics.ListAPIView):
    queryset = WebsiteImage.objects.all()
    serializer_class = WebsiteImageSerializer
    pagination_class = ResultSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['image_url']
    ordering_fields = ['id', 'created_at', 'updated_at']
    ordering = ['created_at']


class WebsiteImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = WebsiteImage.objects.all()
    serializer_class = WebsiteImageSerializer


class ImageDownloadView(APIView):

    def get(self, request, name, format=None):
        name = "images/" + name
        img = WebsiteImage.objects.get(image=name)
        document = open(img.image.path, 'rb')
        response = HttpResponse(FileWrapper(document), content_type='application/msword')
        response['Content-Disposition'] = 'attachment; filename="%s"' % name
        return response
