import json
import logging
from os.path import basename
from typing import List, Text
from urllib.parse import urlsplit

import requests
from celery import shared_task
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import transaction, DatabaseError
from django_pglocks import advisory_lock

from project import settings
from website_content_extractor.models import QueueTask, WebsiteText, WebsiteImage
from website_content_extractor.utils import get_text_from_html, get_url_images_from_html

logger = logging.getLogger(__name__)


@shared_task(autoretry_for=(Exception,), retry_backoff=10, retry_kwargs={'max_retries': 2})
def extract_website():
    with advisory_lock(lock_id=settings.CELERY_LOCK_ID, wait=False) as acquired:
        if not acquired:
            logger.info("already running task: extract_website; exit")
            return

        tasks = QueueTask.objects.filter(state=QueueTask.TaskState.PENDING.value).order_by('created_at')
        save_website_content(tasks)


def save_website_content(tasks: List[QueueTask]):
    try:
        with transaction.atomic():
            for task in tasks:
                if task.get_image:
                    urls = get_url_images_from_html(task.url)
                    save_images(urls, task)
                    logger.info("Saved all images from task id: %s" % task.pk)
                if task.get_text:
                    texts = get_text_from_html(task.url) or []
                    WebsiteText.objects.create(text=json.dumps(texts), task=task)
                    logger.info("Saved all texts from task id: %s" % task.pk)
                task.state = QueueTask.TaskState.SUCCESS.value
                task.save()
    except DatabaseError as e:
        logger.error("Database error: %s" % e)


def save_images(urls: List[Text], task: QueueTask):
    try:
        for url in urls:
            with NamedTemporaryFile() as tf:
                r = requests.get(url, stream=True)
                for chunk in r.iter_content(chunk_size=4096):
                    tf.write(chunk)
                tf.seek(0)
                img = WebsiteImage(image_url=url, task=task)
                img.image.save(basename(urlsplit(url).path), File(tf))
                logger.info("Successfully saved image %s" % urlsplit(url).path)
    except Exception as e:
        logger.error("Error during saving image: %s" % e)
