from typing import List, Optional, Union

import aiohttp

from fastapi import APIRouter, Depends, Body, Path, Query, status, Response

from bo_shared.models.scheduler import (
    CronJobResponse,
    CronJobPatch,
    CronJobPost
)

from internal.utils import request
from config import API_SERVER_USER, SCHEDULER_HOST

router = APIRouter()

__all__ = ('router',)


@router.post("/", response_model=CronJobResponse)
async def add_job(
        response: Response,
        job: CronJobPost = Body(
            ...,
            title='Job to be added to scheduling service'
        )
):
    url = f'{SCHEDULER_HOST}/api/cron'

    data, _, _, _ = await request(
        method='post',
        url=url,
        json=job.dict(exclude_unset=True),
        response=response
    )

    return data


@router.get("/", response_model=List[CronJobResponse])
async def get_jobs(
        response: Response,
        label: Optional[str] = Query(..., title='custom label if provided')
):
    url = f'{SCHEDULER_HOST}/api/cron'
    data, _, _, _ = await request(
        method='get',
        url=url,
        params={'label': label},
        response=response
    )
    return data


@router.get("/{job_id}", response_model=CronJobResponse)
async def get_job(
        response: Response,
        job_id: str = Path(..., title='Job id to retrieve')
):
    url = f'{SCHEDULER_HOST}/api/cron/{job_id}'
    data, _, _, _ = await request(
        method='get',
        url=url,
        response=response
    )

    return data


@router.patch("/{job_id}", response_model=CronJobResponse)
async def edit_job(
        response: Response,
        job_id: str = Path(..., title='Job id to edit'),
        job: CronJobPatch = Body(..., title='Fields to update')
):
    url = f'{SCHEDULER_HOST}/api/cron/{job_id}'
    data, _, _, _ = await request(
        method='patch',
        url=url,
        json=job.dict(exclude_unset=True),
        response=response
    )


    return data


@router.delete("/{job_id}", response_model=CronJobResponse,
               status_code=status.HTTP_200_OK)
async def delete_job(
        response: Response,
        job_id: str = Path(..., title='Job id to delete')
):
    url = f'{SCHEDULER_HOST}/api/cron/{job_id}'
    data, _, _, _ = await request(
        method='delete',
        url=url,
        response=response
    )

    return data
