from fastapi import APIRouter, Depends, Body, Path

from internal import CronHandler
from data import CronJob

from config import SCHEDULER_USER

router = APIRouter(
    prefix="/api/cron"
)

__all__ = ('router',)


async def get_cron_handler():
    return CronHandler(
        user=SCHEDULER_USER
    )


@router.post("/", response_model=CronJob)
async def add_job(
        cron_handler: CronHandler = Depends(get_cron_handler),
        job: CronJob = Body(..., title='Job to be added to scheduling service')
):
    return job


@router.get("/{job_id}", response_model=CronJob)
async def get_job(
        cron_handler: CronHandler = Depends(get_cron_handler),
        job_id: str = Path(..., title='Job id to retrieve')
):
    # job = cron_handler.get_job_by_id(
    #     job_id=job_id
    # )
    # cron_job = CronJob(
    #     id=job_id,
    #     enable=job.is_enabled(),
    #
    # )

    return None


@router.put("/{job_id}", response_model=CronJob)
async def edit_job(
        cron_handler: CronHandler = Depends(get_cron_handler)
):
    pass


@router.delete("/{job_id}", response_model=CronJob)
async def delete_job(
        cron_handler: CronHandler = Depends(get_cron_handler)
):
    pass
