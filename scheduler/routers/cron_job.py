from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Body, Path, status

from internal import CronHandler
from data import CronJob, CronJobRequest, CronJobResponse

from config import SCHEDULER_USER

router = APIRouter(
    prefix="/api/cron"
)

__all__ = ('router',)


async def get_cron_handler():
    return CronHandler(
        user=SCHEDULER_USER
    )


@router.post("/", response_model=CronJobResponse)
async def add_job(
        cron_handler: CronHandler = Depends(get_cron_handler),
        job: CronJobRequest = Body(
            ...,
            title='Job to be added to scheduling service'
        )
):
    cron_job = CronJob(**job.dict())
    cron_job.generate_full_command()

    cron_handler.add_job(
        cron_job=cron_job
    )

    return cron_job


@router.get("/", response_model=List[CronJobResponse])
async def get_jobs(
        cron_handler: CronHandler = Depends(get_cron_handler)
):
    jobs = cron_handler.get_all_jobs()

    return jobs


@router.get("/{job_id}", response_model=CronJobResponse)
async def get_job(
        cron_handler: CronHandler = Depends(get_cron_handler),
        job_id: UUID = Path(..., title='Job id to retrieve')
):
    job = cron_handler.get_job_by_id(
        job_id=str(job_id)
    )

    return job


@router.put("/{job_id}", response_model=CronJobResponse)
async def edit_job(
        cron_handler: CronHandler = Depends(get_cron_handler)
):
    pass


@router.delete("/{job_id}", response_model=CronJobResponse,
               status_code=status.HTTP_200_OK)
async def delete_job(
        cron_handler: CronHandler = Depends(get_cron_handler),
        job_id: UUID = Path(..., title='Job id to delete')
):
    job = cron_handler.get_job_by_id(str(job_id))

    cron_handler.delete_job(job_id=str(job_id))

    return job
