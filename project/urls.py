"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from website_content_extractor.views import QueueTaskList, WebsiteTextList, WebsiteImageList, \
    QueueTaskDetail, WebsiteTextDetail, WebsiteImageDetail, ImageDownloadView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tasks/', QueueTaskList.as_view(), name='api-tasks'),
    path('api/tasks/<pk>', QueueTaskDetail.as_view(), name='api-task'),
    path('api/texts/', WebsiteTextList.as_view(), name='api-texts'),
    path('api/texts/<pk>', WebsiteTextDetail.as_view(), name='api-text'),
    path('api/images/', WebsiteImageList.as_view(), name='api-images'),
    path('api/images/<pk>', WebsiteImageDetail.as_view(), name='api-image'),
    path('media/images/<name>', ImageDownloadView.as_view(), name='api-image-download'),
]
