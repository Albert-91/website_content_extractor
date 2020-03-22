from enum import Enum
from typing import List

from django.contrib.postgres.fields import JSONField
from django.core.validators import RegexValidator
from django.db import models
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

    url = models.URLField(_("URL"), blank=False, max_length=1000, null=False, validators=[RegexValidator(
        regex='(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})',
        message='Invalid URL'
    )])
    get_text = models.BooleanField(verbose_name=_("get texts"), default=True)
    get_image = models.BooleanField(verbose_name=_("get images"), default=True)
    state = models.CharField(
        verbose_name=_("state"), choices=TaskState.value_name_pairs(), max_length=20, default=TaskState.PENDING.value,
    )

    class Meta:
        db_table = "queue_tasks"
        verbose_name = _("queue task")
        verbose_name_plural = _("queue tasks")


class WebsiteImage(Timestamps, models.Model):
    image = models.ImageField(verbose_name=_("image"), upload_to='images/', null=True)
    image_url = models.URLField(verbose_name=_("image url"), blank=True, max_length=1000)
    task = models.ForeignKey(to=QueueTask, on_delete=models.CASCADE, related_name='images')

    class Meta:
        db_table = "website image"
        verbose_name = _("website image")
        verbose_name_plural = _("website images")


class WebsiteText(Timestamps, models.Model):
    text = JSONField(verbose_name=_("texts"), default=list, blank=True, null=False)
    task = models.ForeignKey(to=QueueTask, on_delete=models.CASCADE, related_name='texts')

    class Meta:
        db_table = "website text"
        verbose_name = _("website text")
        verbose_name_plural = _("website texts")
