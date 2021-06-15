from typing import List, Optional

from fastapi import APIRouter, Body, Path, Query, Response, status

from data.db import (
    NameSpace as NameSpaceDB,
    Token as TokenDB
)

from data.pydantic import (
    NameSpaceAdminResponse,
    NameSpacePost,
    TokenResponse,
    NameSpaceResponse,
    NameSpacePatch
)

from exceptions import NameSpaceExists, TokenNotValid

router = APIRouter()


@router.get('/token/{token_key}', response_model=NameSpaceResponse)
async def get_namespace(
        token_key: str = Path(
            ...,
            title='key of the token',
            max_length=64
        )
):
    token = await TokenDB.filter(
        key=token_key,
        valid=True
    ).prefetch_related('namespace').first()

    if not token:
        raise TokenNotValid()

    return token.namespace


@router.get('/namespace', response_model=List[NameSpaceAdminResponse])
async def get_namespaces():
    namespaces = await NameSpaceDB.all().prefetch_related(
        'tokens'
    )

    responses = await NameSpaceAdminResponse.module_response_from_db_model_list(
        namespaces
    )

    return responses


@router.post('/namespace', response_model=NameSpaceResponse)
async def create_namespace(
        namespace: NameSpacePost = Body(
            ...,
            title='namespace to create',
        )
):
    exists = await NameSpaceDB.filter(
        name=namespace.name
    ).exists()
    if exists:
        raise NameSpaceExists()

    namespace = await NameSpaceDB.create(
        name=namespace.name
    )

    return namespace


@router.delete('/namespace/{namespace_name}', response_model=NameSpaceResponse)
async def delete_namespace(
        namespace_name: str = Path(
            ...,
            title='namespace name',
            max_length=256
        )
):
    namespace = await NameSpaceDB.get(
        name=namespace_name
    )

    await NameSpaceDB.filter(
        name=namespace_name
    ).delete()

    return namespace


@router.patch('/namespace/{namespace_name}', response_model=NameSpaceResponse)
async def edit_namespace(
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
    namespace_ = await NameSpaceDB.get(
        name=namespace_name
    )
    namespace_.name = namespace.name
    await namespace_.save()

    return namespace_


@router.post('/token', response_model=TokenResponse)
async def create_token(
        namespace_name: str = Body(
            ...,
            title='namespace name',
            max_length=256,
            embed=True
        )
):
    namespace = await NameSpaceDB.get(
        name=namespace_name
    )

    token = await TokenDB.create(
        namespace=namespace
    )

    return token


@router.patch('/token/{token_key}', response_model=TokenResponse)
async def toggle_token_validity(
        token_key: str = Path(
            ...,
            title='token key',
            max_length=64
        )
):
    token = await TokenDB.get(
        key=token_key
    )
    token.valid = not token.valid
    await token.save()
    await token.fetch_related('namespace')

    return token


@router.delete('/token/{token_key}', response_model=TokenResponse)
async def delete_token(
        token_key: str = Path(
            ...,
            title='token key',
            max_length=64
        )
):
    token = await TokenDB.get(
        key=token_key
    )

    await token.fetch_related('namespace')

    await TokenDB.filter(
        key=token_key
    ).delete()

    return token
