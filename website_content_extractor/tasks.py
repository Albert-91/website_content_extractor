import logging
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import List, Text
from urllib.parse import urlsplit

import requests
from celery import shared_task
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

        tasks = QueueTask.get_tasks_to_run()
        if tasks:
            save_website_content(tasks)


def save_website_content(tasks: List[QueueTask]):
    try:
        with transaction.atomic():
            for task in tasks:
                if task.get_image:
                    urls = get_url_images_from_html(task.url) or []
                    save_images(urls, task)
                    logger.info("Saved all images from task id: %s" % task.pk)
                if task.get_text:
                    texts = get_text_from_html(task.url) or []
                    WebsiteText.save_texts(texts, task)
                    logger.info("Saved all texts from task id: %s" % task.pk)
                task.set_success_state()
    except DatabaseError as e:
        logger.error("Database error: %s" % e)


def save_images(urls: List[Text], task: QueueTask):
    try:
        get_image_task = partial(get_image, task=task)
        with ThreadPoolExecutor() as executor:
            executor.map(get_image_task, urls)
    except Exception as e:
        logger.error("Error during saving image: %s" % e)


def get_image(url: Text, task: QueueTask):
    with NamedTemporaryFile() as tf:
        r = requests.get(url, stream=True)
        for chunk in r.iter_content(chunk_size=4096):
            tf.write(chunk)
        tf.seek(0)
        img = WebsiteImage(image_url=url, task=task)
        img.save_image(tf)
        logger.info("Successfully saved image %s" % urlsplit(url).path)
