import json
import logging

from celery import shared_task
from django.db import transaction

from website_content_extractor.models import QueueTask, WebsiteText, WebsiteImage

from website_content_extractor.utils import get_text_from_html, get_url_images_from_html

logger = logging.getLogger(__name__)


@shared_task(autoretry_for=(Exception,), retry_backoff=10, retry_kwargs={'max_retries': 2})
def extract_website():
    with transaction.atomic():
        # with advisory_lock(lock_id=LOCK_ID, wait=False) as acquired:
        # if not acquired:
        #     logger.info("already running task: synchronize_conversations_for_fanpages; exit")
        #     return
        tasks = QueueTask.objects.filter(state=QueueTask.TaskState.PENDING.value).order_by('created_at')
        for task in tasks:
            if task.get_image:
                urls = get_url_images_from_html(task.url)
                save_images(urls)
            if task.get_text:
                texts = get_text_from_html(task.url) or []
                WebsiteText.objects.create(text=json.dumps(texts), task=task)
            task.state = QueueTask.TaskState.SUCCESS.value
            task.save()


def save_images(urls):
    pass