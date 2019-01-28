import time

from config import HOST_IP, NOTIFY_URL, MOBILE_NUMBER
from celery import Celery
from celery.schedules import crontab
import sys
import os
BROKER_URI = 'redis://%s:6379/6' % "127.0.0.1"
BACKEND_URI = 'redis://%s:6379/5' % "127.0.0.1"

worker = Celery('tasks', broker=BROKER_URI, backend=BACKEND_URI)

worker.conf.update(
    timezone='Asia/Shanghai',
    enable_utc=True,
    beat_schedule={
        "morning_msg_1": {
            "task": "tasks.notify_dingding",
            "schedule": 2,
            "args": ("sh ./excspidershell",)
        },
        "morning_msg_2": {
            "task": "tasks.notify_dingding",
            "schedule": crontab(minute=0, hour=3),
            "args": ("sh ./excspidershell",)
        }
    }
)

@worker.task
def notify_dingding(msg):

    os.system(msg)
    print(msg)