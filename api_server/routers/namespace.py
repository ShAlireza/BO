from typing import List, Optional, Union, Dict

import aiohttp

from fastapi import APIRouter, Depends, Body, Path, Query, status, Response

from bo_shared.models.namespace import (
    NameSpaceResponse,
    NameSpaceAdminResponse,
    NameSpacePatch,
    NameSpacePost,
    TokenResponse
)

from internal.utils import request

from config import NAMESPACE_HOST

router = APIRouter()

__all__ = ('router',)


@router.get('/token/{token_key}',
            response_model=Union[NameSpaceResponse, Dict[str, str]])
async def get_namespace(
        response: Response,
        token_key: str = Path(
            ...,
            title='key of the token',
            max_length=64
        )
):
    url = f'{NAMESPACE_HOST}/api/token/{token_key}'

    data, _, _, _ = await request(
        method='get',
        url=url,
        response=response
    )

    return data


@router.get('/namespace',
            response_model=Union[List[NameSpaceResponse], Dict[str, str]])
async def get_namespaces(
        response: Response
):
    url = f'{NAMESPACE_HOST}/api/namespace'

    data, _, _, _ = await request(
        method='get',
        url=url,
        response=response
    )

    return data


@router.post('/namespace',
             response_model=Union[NameSpaceResponse, Dict[str, str]])
async def create_namespace(
        response: Response,
        namespace: NameSpacePost = Body(
            ...,
            title='namespace to create',
        )
):
    url = f'{NAMESPACE_HOST}/api/namespace'

    data, _, _, _ = await request(
        method='post',
        url=url,
        json=namespace.dict(),
        response=response
    )

    return data


@router.patch('/namespace/{namespace_name}',
              response_model=Union[NameSpaceResponse, Dict[str, str]])
async def edit_namespace(
        response: Response,
        namespace_name: str = Path(
            ...,
            title='namespace name',
            max_length=256
        ),
        namespace: NameSpacePatch = Body(
            ...,
            title='namespace name'
        )
):
    url = f'{NAMESPACE_HOST}/api/namespace/{namespace_name}'

    data, _, _, _ = await request(
        method='patch',
        url=url,
        json=namespace.dict(),
        response=response
    )

    return data


@router.post('/token',
             response_model=Union[TokenResponse, Dict[str, str]])
async def create_token(
        response: Response,
        namespace_name: str = Body(
            ...,
            title='namespace name',
            max_length=256,
            embed=True
        )
):
    url = f'{NAMESPACE_HOST}/api/token'

    data, _, _, _ = await request(
        method='post',
        url=url,
        json={
            'namespace_name': namespace_name
        },
        response=response
    )

    return data


@router.patch('/token/{token_key}',
              response_model=Union[TokenResponse, Dict[str, str]])
async def toggle_token_validity(
        response: Response,
        token_key: str = Path(
            ...,
            title='token key',
            max_length=64
        )
):
    url = f'{NAMESPACE_HOST}/api/token/{token_key}'

    data, _, _, _ = await request(
        method='patch',
        url=url,
        response=response
    )

    return data


@router.delete('/token/{token_key}',
               response_model=Union[TokenResponse, Dict[str, str]])
async def delete_token(
        response: Response,
        token_key: str = Path(
            ...,
            title='token key',
            max_length=64
        )
):
    url = f'{NAMESPACE_HOST}/api/token/{token_key}'

    data, _, _, _ = await request(
        method='delete',
        url=url,
        response=response
    )

    return data
