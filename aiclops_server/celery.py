# celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from kombu import Queue
from celery.schedules import crontab

# 기본 장고파일 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aiclops_server.settings')
app = Celery('aiclops_server')
app.config_from_object('django.conf:settings', namespace='CELERY')

# 작업 큐 생성
app.conf.task_queues = (
    Queue("Q_API", routing_key="API.#"),
    Queue("Q_AI", routing_key="AI.#"),
)
#등록된 장고 앱 설정에서 task 불러오기
app.autodiscover_tasks()

