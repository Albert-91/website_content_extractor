import logging
from wsgiref.util import FileWrapper

from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, ListCreateAPIView
from rest_framework.views import APIView

from website_content_extractor.models import QueueTask, WebsiteText, WebsiteImage
from website_content_extractor.pagination import ResultSetPagination
from website_content_extractor.serializers import QueueTaskSerializer, WebsiteTextSerializer, WebsiteImageSerializer

logger = logging.getLogger(__name__)


class QueueTaskList(ListCreateAPIView):
    queryset = QueueTask.objects.all()
    serializer_class = QueueTaskSerializer
    pagination_class = ResultSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ('state', 'get_text', 'get_image')
    search_fields = ['url']
    ordering_fields = ['id', 'created_at', 'updated_at']
    ordering = ['created_at']


class QueueTaskDetail(RetrieveUpdateDestroyAPIView):
    queryset = QueueTask.objects.all()
    serializer_class = QueueTaskSerializer


class WebsiteTextList(ListAPIView):
    queryset = WebsiteText.objects.all()
    serializer_class = WebsiteTextSerializer
    pagination_class = ResultSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['text']
    ordering_fields = ['id', 'created_at', 'updated_at']
    ordering = ['created_at']


class WebsiteTextDetail(RetrieveUpdateDestroyAPIView):
    queryset = WebsiteText.objects.all()
    serializer_class = WebsiteTextSerializer


class WebsiteImageList(ListAPIView):
    queryset = WebsiteImage.objects.all()
    serializer_class = WebsiteImageSerializer
    pagination_class = ResultSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['image_url']
    ordering_fields = ['id', 'created_at', 'updated_at']
    ordering = ['created_at']


class WebsiteImageDetail(RetrieveUpdateDestroyAPIView):
    queryset = WebsiteImage.objects.all()
    serializer_class = WebsiteImageSerializer


class ImageDownloadView(APIView):

    def get(self, request, name):
        name = "images/" + name
        img = WebsiteImage.objects.get(image=name)
        document = open(img.image.path, 'rb')
        response = HttpResponse(FileWrapper(document), content_type='application/msword')
        response['Content-Disposition'] = 'attachment; filename="%s"' % name
        return response
