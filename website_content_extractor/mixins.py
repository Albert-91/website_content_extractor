from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Timestamps(models.Model):

    created_at = models.DateTimeField(
        _("created at"), auto_now_add=timezone.now, editable=False, blank=True,
    )
    updated_at = models.DateTimeField(
        _("last updated at"), auto_now=timezone.now, editable=False, blank=True,
    )

    class Meta:
        abstract = True
