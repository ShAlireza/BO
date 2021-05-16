import uuid
from datetime import datetime
from typing import List, Optional, Union, Any
from uuid import UUID

from pydantic import BaseModel, Field, validator, ValidationError

from config import PYTHONPATH

__all__ = ('CronJob', 'CronJobPost', 'CronJobResponse', 'CronJobPatch')

CRON_TIME_REGEX = r'^((\d+,)+\d+|([*]/\d+)|(\d+(/|-)\d+)|\d+|[*])$'


class CronJobBase(BaseModel):
    enable: Optional[bool] = Field(
        True,
        title="Enable job"
    )

    technology: str = Field(
        ...,
        title='CronJob technology',
        max_length=128
    )

    host: str = Field(
        ...,
        title='Service host'
    )

    port: Optional[int] = Field(
        None,
        title='Service host port'
    )

    minute: str = Field(
        ...,
        title='Cron job minute field',
        regex=CRON_TIME_REGEX
    )

    hour: str = Field(
        '*',
        title='Cron job hour field',
        regex=CRON_TIME_REGEX
    )

    day_of_month: str = Field(
        '*',
        title='Cron job day of the month field',
        regex=CRON_TIME_REGEX
    )

    month: str = Field(
        '*',
        title='Cron job month field',
        regex=CRON_TIME_REGEX
    )

    day_of_week: str = Field(
        '*',
        title='Cron job day of the week field',
        regex=CRON_TIME_REGEX
    )


class CronJob(CronJobBase):
    id: UUID = Field(
        ...,
        title="Cron job unique id",
        default_factory=lambda: str(uuid.uuid4())
    )

    created: str = Field(
        ...,
        title='Job create time',
        default_factory=lambda: str(datetime.now())
    )

    full_command: str = Field(
        None,
        title='Cron job command to execute'
    )

    def generate_full_command(self):
        self.full_command = (f'{PYTHONPATH}/internal/event_push.py '
                             f'--tech {self.technology} '
                             f'--host {self.host} '
                             f'--port {self.port}')
        return self.full_command


class CronJobPost(CronJobBase):
    pass


class CronJobPatch(CronJobBase):
    technology: Optional[str] = Field(
        None,
        title='CronJob technology',
        max_length=128
    )

    host: Optional[str] = Field(
        None,
        title='Service host'
    )

    minute: Optional[int] = Field(
        None,
        title='Cron job minute field',
        regex=CRON_TIME_REGEX
    )


class CronJobResponse(CronJobBase):
    id: UUID = Field(
        ...,
        title='Cron job unique id'
    )
    
    created: str = Field(
        ...,
        title='Job create time'
    )
