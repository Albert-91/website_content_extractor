import os
from datetime import timedelta
from project import settings
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
redis = settings.CELERY_BROKER_URL
app = Celery("project", broker=redis, backend=redis)
app.autodiscover_tasks()

app.conf.task_serializer = settings.CELERY_TASK_SERIALIZER
app.conf.result_serializer = settings.CELERY_RESULT_SERIALIZER
app.conf.accept_content = settings.CELERY_ACCEPT_CONTENT

app.conf.enable_utc = False
app.conf.timezone = os.environ.get('TIME_ZONE')

app.conf.create_dirs = True
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.task_create_missing_queues = True
app.conf.worker_prefetch_multiplier = 2
app.conf.task_queue_max_priority = 100
app.conf.task_default_queue = "default"
app.conf.task_default_exchange = "default"
app.conf.task_default_routing_key = "default"

app.conf.beat_schedule = {}

# start enabled celery_reports tasks related to sftp reports upload
if os.environ.get('CELERY_EXTRACTING_WEBSITE_PROCESS_ENABLED'):
    app.conf.beat_schedule['extracting_website_process'] = {
       'task': 'website_content_extractor.tasks.extract_website',
       'schedule': timedelta(minutes=int(os.environ.get('CELERY_EXTRACTING_WEBSITE_PROCESS_INTERVAL'))),
    }
