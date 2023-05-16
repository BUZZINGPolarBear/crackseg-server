# celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# 기본 장고파일 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aiclops_server.settings')
app = Celery('aiclops_server')
app.config_from_object('django.conf:settings', namespace='CELERY')

#등록된 장고 앱 설정에서 task 불러오기
app.autodiscover_tasks()

# task 함수 주기 설정
# app.conf.beat_schedule = {
#     'printTime': {  # 스케쥴링 이름
#         'task' : 'crackSegmentation.tasks.*', # 수행할 task 설정
#         'schedule': crontab(),  # 인자 없으면 매 분마다 실행
#     }
# }