from typing import List, Optional, Union, Dict

import aiohttp

from fastapi import APIRouter, Depends, Body, Path, Query, status, Response

from bo_shared.models.scheduler import (
    CronJobResponse,
    CronJobPatch,
    CronJobPost
)
from bo_shared.utils.namespace import namespace_token_header

from internal.utils import request
from exceptions import ServiceInstanceNotFound
from config import API_SERVER_USER, SCHEDULER_HOST, MANAGER_HOST

router = APIRouter()

__all__ = ('router',)


@router.post(
    "/",
    response_model=Union[CronJobResponse, Dict]
)
async def add_job(
        response: Response,
        namespace_token: str = Depends(namespace_token_header),
        job: CronJobPost = Body(
            ...,
            title='Job to be added to scheduling service'
        )
):
    url = f'{SCHEDULER_HOST}/api/cron'
    existence_module = f'{MANAGER_HOST}/api/module/{job.technology}/exists'
    _, status_code, _, _ = await request(
        method='post',
        url=existence_module,
        json={
            'host': job.host,
            'port': job.port
        },
        headers={
            'namespace-token': namespace_token
        }
    )
    if status_code == status.HTTP_404_NOT_FOUND:
        raise ServiceInstanceNotFound()
    print(status_code)

    print(job.dict(), '<==============================')
    data, _, _, _ = await request(
        method='post',
        url=url,
        json=job.dict(exclude_unset=True),
        response=response,
        headers={
            'namespace-token': namespace_token
        }
    )

    return data


@router.get(
    "/",
    response_model=Union[List[CronJobResponse], Dict]
)
async def get_jobs(
        response: Response,
        namespace_token: str = Depends(namespace_token_header),
):
    url = f'{SCHEDULER_HOST}/api/cron'
    data, _, _, _ = await request(
        method='get',
        url=url,
        response=response,
        headers={
            'namespace-token': namespace_token
        }
    )
    return data


@router.get(
    "/{job_id}",
    response_model=Union[CronJobResponse, Dict]
)
async def get_job(
        response: Response,
        namespace_token: str = Depends(namespace_token_header),
        job_id: str = Path(..., title='Job id to retrieve')
):
    url = f'{SCHEDULER_HOST}/api/cron/{job_id}'
    data, _, _, _ = await request(
        method='get',
        url=url,
        response=response,
        headers={
            'namespace-token': namespace_token
        }
    )

    return data


@router.patch(
    "/{job_id}",
    response_model=Union[CronJobResponse, Dict]
)
async def edit_job(
        response: Response,
        namespace_token: str = Depends(namespace_token_header),
        job_id: str = Path(..., title='Job id to edit'),
        job: CronJobPatch = Body(..., title='Fields to update')
):
    url = f'{SCHEDULER_HOST}/api/cron/{job_id}'
    data, _, _, _ = await request(
        method='patch',
        url=url,
        json=job.dict(exclude_unset=True),
        response=response,
        headers={
            'namespace-token': namespace_token
        }
    )

    return data


@router.delete(
    "/{job_id}",
    response_model=Union[CronJobResponse, Dict]
)
async def delete_job(
        response: Response,
        namespace_token: str = Depends(namespace_token_header),
        job_id: str = Path(..., title='Job id to delete')
):
    url = f'{SCHEDULER_HOST}/api/cron/{job_id}'
    data, _, _, _ = await request(
        method='delete',
        url=url,
        response=response,
        headers={
            'namespace-token': namespace_token
        }
    )

    return data
