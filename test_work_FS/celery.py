import os

from celery import Celery
from test_work_FS.settings import CELERY_BROKER_URL

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_work_FS.settings')
app = Celery('test_work_FS', broker=CELERY_BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
