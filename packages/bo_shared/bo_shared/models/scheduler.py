import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

try:
    from config import PYTHONPATH
except ImportError:
    raise ImportError('PYTHONPATH not found in config file')

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
        "*",
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

    label: Optional[str] = Field(
        None,
        title='Custom optional label for job'
    )

    @staticmethod
    def instance_from_tortoise_model(model):
        key_values = {k: getattr(model, k) for k in model._meta.fields}
        return CronJob(**key_values)


class CronJob(CronJobBase):
    id: str = Field(
        title="Cron job unique id",
        default_factory=lambda: str(uuid.uuid4())
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


class CronJobResponse(CronJobBase):
    id: str = Field(
        ...,
        title='Cron job unique id'
    )

    created_at: datetime = Field(
        ...,
        title='Job create time'
    )
    updated_at: datetime = Field(
        ...,
        title='Job last update time'
    )

    class Config:
        orm_mode = True
