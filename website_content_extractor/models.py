import json
from enum import Enum
from os.path import basename
from typing import List
from urllib.parse import urlsplit

from django.contrib.postgres.fields import JSONField
from django.core.files import File
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import QuerySet
from django.utils.translation import ugettext_lazy as _

from website_content_extractor.mixins import Timestamps


class QueueTask(Timestamps, models.Model):

    class TaskState(Enum):
        PENDING = "pending"
        FAILURE = "failure"
        SUCCESS = "success"

        @classmethod
        def value_name_pairs(cls) -> List:
            return list(map(lambda state: (state.value, state.name), cls))

    regex = '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'
    url = models.URLField(_("URL"), blank=False, max_length=1000, null=False, validators=[RegexValidator(
        regex=regex,
        message='Invalid URL'
    )])
    get_text = models.BooleanField(verbose_name=_("get texts"), default=False, blank=True)
    get_image = models.BooleanField(verbose_name=_("get images"), default=False, blank=True)
    state = models.CharField(
        verbose_name=_("state"), choices=TaskState.value_name_pairs(), max_length=20, default=TaskState.PENDING.value, blank=True
    )

    class Meta:
        db_table = "queue_tasks"
        verbose_name = _("queue task")
        verbose_name_plural = _("queue tasks")

    @classmethod
    def get_tasks_to_run(cls) -> List[QuerySet]:
        return cls.objects.filter(state=cls.TaskState.PENDING.value).order_by('created_at')

    def set_success_state(self):
        self.state = QueueTask.TaskState.SUCCESS.value
        self.save()


class WebsiteImage(Timestamps, models.Model):
    image = models.ImageField(verbose_name=_("image"), upload_to='images/', null=True)
    image_url = models.URLField(verbose_name=_("image url"), blank=True, max_length=1000)
    task = models.ForeignKey(to=QueueTask, on_delete=models.CASCADE, related_name='images')

    class Meta:
        db_table = "website image"
        verbose_name = _("website image")
        verbose_name_plural = _("website images")

    def save_image(self, temp_file):
        img = WebsiteImage(image_url=self.image_url, task=self.task)
        img.image.save(basename(urlsplit(self.image_url).path), File(temp_file))


class WebsiteText(Timestamps, models.Model):
    text = JSONField(verbose_name=_("texts"), default=list, blank=True, null=False)
    task = models.ForeignKey(to=QueueTask, on_delete=models.CASCADE, related_name='texts')

    class Meta:
        db_table = "website text"
        verbose_name = _("website text")
        verbose_name_plural = _("website texts")

    @classmethod
    def save_texts(cls, texts, task):
        return cls.objects.create(text=json.dumps(texts), task=task)
