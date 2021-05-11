import uuid
from typing import List, Optional, Union, Any

from pydantic import BaseModel, Field, validator, ValidationError

__all__ = ('CronJob',)


class CronJob(BaseModel):
    id: int = Field(
        ...,
        title="Cron job unique id",
        default_factory=lambda: str(uuid.uuid4())
    )
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

    port: Optional[str] = Field(
        None,
        title='Service host port'
    )

    minute: str = Field(
        ...,
        title='Cron job minute field',
        regex=r'^((\d+,)+\d+|([*]/\d+)|(\d+(/|-)\d+)|\d+|[*])$'
    )

    hour: str = Field(
        '*',
        title='Cron job hour field',
        regex=r'^((\d+,)+\d+|([*]/\d+)|(\d+(/|-)\d+)|\d+|[*])$'
    )

    day_of_month: str = Field(
        '*',
        title='Cron job day of the month field',
        regex=r'^((\d+,)+\d+|([*]/\d+)|(\d+(/|-)\d+)|\d+|[*])$'
    )

    month: str = Field(
        '*',
        title='Cron job month field',
        regex=r'^((\d+,)+\d+|([*]/\d+)|(\d+(/|-)\d+)|\d+|[*])$'
    )

    day_of_week: str = Field(
        '*',
        title='Cron job day of the week field',
        regex=r'^((\d+,)+\d+|([*]/\d+)|(\d+(/|-)\d+)|\d+|[*])$'
    )

    full_command: str = Field(
        None,
        title='Cron job command to execute'
    )
