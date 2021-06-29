from typing import List, Optional, Union, Dict

import aiohttp

from fastapi import APIRouter, Depends, Body, Path, Query, status, Response

from bo_shared.models.manager import (
    ModuleResponse,
    SecretKeyResponse,
    ServiceInstanceDataResponse,
    ServiceInstanceData,
    ServiceInstanceDataPatch
)
from bo_shared.utils.namespace import namespace_token_header

from internal.utils import request
from config import API_SERVER_USER, MANAGER_HOST

router = APIRouter()

__all__ = ('router',)


@router.get(
    "/",
    response_model=Union[List[ModuleResponse], Dict]
)
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


@router.post(
    "/secret-key",
    response_model=Union[SecretKeyResponse, Dict]
)
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


@router.get(
    "/secret-key",
    response_model=Union[List[SecretKeyResponse], Dict]
)
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


@router.patch(
    "/secret-key/{secret_key_id}",
    response_model=Union[SecretKeyResponse, Dict]
)
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


@router.delete(
    "/secret-key/{secret_key_id}",
    response_model=Union[SecretKeyResponse, Dict]
)
async def delete_secret_key(
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


@router.get(
    "/{module_name}",
    response_model=Union[List[ServiceInstanceDataResponse], Dict]
)
async def get_service_instances_data(
        response: Response,
        namespace_token: str = Depends(namespace_token_header),
        module_name: str = Path(
            ...,
            title='module name for adding service instance'
        )
):
    url = f'{MANAGER_HOST}/api/module/{module_name}'
    data, _, _, _ = await request(
        method='get',
        url=url,
        response=response,
        headers={
            'namespace-token': namespace_token
        }
    )

    return data


@router.post("/{module_name}",
             response_model=Union[ServiceInstanceDataResponse, Dict])
async def add_service_instance_data(
        response: Response,
        namespace_token: str = Depends(namespace_token_header),
        module_name: str = Path(
            ...,
            title='module name for adding service instance'
        ),
        service_instance: ServiceInstanceData = Body(
            ...,
            title='service instance data'
        )
):
    url = f'{MANAGER_HOST}/api/module/{module_name}'
    data, _, _, _ = await request(
        method='post',
        url=url,
        json=service_instance.dict(exclude_unset=True),
        response=response,
        headers={
            'namespace-token': namespace_token
        }
    )

    return data


@router.patch(
    "/{module_name}/{service_instance_id}",
    response_model=Union[ServiceInstanceDataResponse, Dict]
)
async def edit_service_instance_data(
        response: Response,
        namespace_token: str = Depends(namespace_token_header),
        module_name: str = Path(
            ...,
            title='module name for adding service instance'
        ),
        service_instance_id: int = Path(
            ...,
            title='service instance id',
            ge=0
        ),
        service_instance: ServiceInstanceDataPatch = Body(
            ...,
            title='service instance data'
        )
):
    url = f'{MANAGER_HOST}/api/module/{module_name}/{service_instance_id}'
    data, _, _, _ = await request(
        method='patch',
        url=url,
        json=service_instance.dict(exclude_unset=True),
        response=response,
        headers={
            'namespace-token': namespace_token
        }
    )

    return data


@router.post("/{module_name}/detail",
             response_model=Union[ServiceInstanceDataResponse, Dict])
async def get_service_instance_data(
        response: Response,
        namespace_token: str = Depends(namespace_token_header),
        module_name: str = Path(
            ...,
            title='module name'
        ),
        host: str = Body(
            ...,
            title='service instance host ip'
        ),
        port: int = Body(
            ...,
            title='service instance port'
        )
):
    url = f'{MANAGER_HOST}/api/module/{module_name}/detail'
    data, _, _, _ = await request(
        method='post',
        url=url,
        json={
            'host': host,
            'port': port
        },
        response=response,
        headers={
            'namespace-token': namespace_token
        }
    )

    return data


@router.delete(
    "/{module_name}/{service_instance_id}",
    response_model=Union[ServiceInstanceDataResponse, Dict]
)
async def delete_service_instance_data(
        response: Response,
        namespace_token: str = Depends(namespace_token_header),
        module_name: str = Path(
            ...,
            title='module name for adding service instance'
        ),
        service_instance_id: int = Path(
            ...,
            title='service instance id',
            ge=0
        )
):
    url = f'{MANAGER_HOST}/api/module/{module_name}/{service_instance_id}'
    data, _, _, _ = await request(
        method='delete',
        url=url,
        response=response,
        headers={
            'namespace-token': namespace_token
        }
    )

    return data
