from typing import List, Optional

from pydantic import BaseModel, Field


class CronJob(BaseModel):
    id: int = Field(
        ...,
        title="Cron job unique id"
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

    port: str = Field(
        None,
        title='Service host port'
    )
