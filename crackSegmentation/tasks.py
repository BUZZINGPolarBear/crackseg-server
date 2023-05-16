# tasks.py
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import datetime

from aiclops_server.celery import app

# test 용 함수
@shared_task
def printTime():
    print("Testtime: ", datetime.now())

@shared_task
def printName(name):
    print(f"Hello {name}")