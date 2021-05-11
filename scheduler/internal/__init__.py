import os

from .cron_job import cron_handler, CronHandler

EVENT_PUSH_PATH = f'{os.getcwd()}/event_push.py'
