from typing import List, Optional, Union

import aiohttp

from fastapi import APIRouter, Depends, Body, Path, Query, status, Response

from bo_shared.models.manager import (
    ModuleResponse,
    SecretKeyResponse,
)

from internal.utils import request
from config import API_SERVER_USER, MANAGER_HOST

router = APIRouter()

__all__ = ('router',)


@router.get("/", response_model=List[ModuleResponse])
async def get_registered(
        response: Response,
):
    url = f'{MANAGER_HOST}/api/module'

    data, _, _, _ = await request(
        method='get',
        url=url,
        response=response
    )

    return data


@router.post("/secret-key", response_model=SecretKeyResponse)
async def create_secret_key(
        response: Response
):
    url = f'{MANAGER_HOST}/api/module/secret-key'
    data, _, _, _ = await request(
        method='post',
        url=url,
        response=response
    )

    return data


@router.get("/secret-key", response_model=List[SecretKeyResponse])
async def get_secret_keys(
        response: Response
):
    url = f'{MANAGER_HOST}/api/module/secret-key'
    data, _, _, _ = await request(
        method='get',
        url=url,
        response=response
    )

    return data


@router.patch("/secret-key/{secret_key_id}", response_model=SecretKeyResponse)
async def toggle_secret_key_validity(
        response: Response,
        secret_key_id: int = Path(..., title='id of secret_key', ge=0)
):
    url = f'{MANAGER_HOST}/api/module/secret-key/{secret_key_id}'
    data, _, _, _ = await request(
        method='patch',
        url=url,
        response=response
    )

    return data


@router.delete("/secret-key/{secret_key_id}", response_model=SecretKeyResponse,
               status_code=status.HTTP_200_OK)
async def delete_job(
        response: Response,
        secret_key_id: int = Path(..., title='id of secret_key', ge=0)
):
    url = f'{MANAGER_HOST}/api/module/secret-key/{secret_key_id}'
    data, _, _, _ = await request(
        method='delete',
        url=url,
        response=response
    )

    return data
