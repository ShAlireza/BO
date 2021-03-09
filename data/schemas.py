from typing import List, Optional

from pydantic import BaseModel, Field


class CronJob(BaseModel):
    job_id: str = Field(
        ...,
        title="Cron job unique id",
        max_length=128
    )
    enable: Optional[bool] = Field(
        True,
        title="Enable job"
    )

    class Config:
        orm_mode = True
