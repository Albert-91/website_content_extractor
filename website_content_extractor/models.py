from enum import Enum
from typing import Generator, Tuple, List

from django.db import models
from django.utils.translation import ugettext_lazy as _

from website_content_extractor.mixins import Timestamps


class QueueTask(Timestamps, models.Model):

    class TaskState(Enum):
        PENDING = "pending"
        FAILURE = "failure"
        DONE = "done"

        @classmethod
        def value_name_pairs(cls) -> List:
            return list(map(lambda state: (state.value, state.name), cls))

    url = models.URLField(_("url"), blank=False, max_length=1000)
    get_text = models.BooleanField(_("get_text"), default=True)
    get_image = models.BooleanField(_("get_image"), default=True)
    state = models.CharField(
        _("state"), choices=TaskState.value_name_pairs(), max_length=20, default=TaskState.PENDING.value,
    )

    class Meta:
        db_table = "queue_tasks"
        verbose_name = _("queue task")
        verbose_name_plural = _("queue tasks")


class WebsiteImage(Timestamps, models.Model):
    image = models.ImageField(_("image"), upload_to='images/', null=True,)
    task = models.ForeignKey(to=QueueTask, on_delete=models.CASCADE)


class WebsiteText(Timestamps, models.Model):
    text = models.TextField(_("text"), null=True)
    task = models.ForeignKey(to=QueueTask, on_delete=models.CASCADE)
