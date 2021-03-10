from typing import List, Optional

from pydantic import BaseModel, Field


class Argument(BaseModel):
    id: int = Field(
        ...,
        title='Argument unique id',
    )
    name: str = Field(
        ...,
        title='Argument name',
        max_length=128
    )
    value: str = Field(
        ...,
        title='Argument value',
        max_length=256
    )

    cron_job_id: int = Field(
        ...,
        title='Related cron job unique id'
    )


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

    arguments: List[Argument] = Field(
        ...,
        title='CronJob arguments passed'
    )

    class Config:
        orm_mode = True
