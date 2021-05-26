from typing import Optional, List

import aiohttp
from aiohttp import ContentTypeError

from fastapi import (
    APIRouter,
    Path,
    Body,
    Query,
    Header,
    Depends,
    Response,
    status,
    Request,
    HTTPException
)

from data.db import (
    Module as ModuleDB,
    ModuleInstance as ModuleInstanceDB,
    Token as TokenDB
)
from data.pydantic import (
    ModuleInstance,
    ModuleResponse,
    Token
)

__all__ = ('router',)

router = APIRouter()


async def validate_login(
        instance: ModuleInstance = Body(
            ...,
            title='module_instance object for module',
            embed=True
        ),
        validation_token: str = Body(
            ...,
            title='module validation_token',
            embed=True,
            max_length=128
        )
):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'http://{instance.host}:{instance.port}/login-validate'
        ) as response:
            try:
                result = await response.json()
            except ContentTypeError as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    if result.get('validation_token') != validation_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='given ip not matched with request host')

    return instance


async def authorize_instance(
        authorization: str = Header('...', regex=r"^Bearer [a-zA-Z0-9]+$")
):
    token_key = authorization[7:]

    token = await TokenDB.get(key=token_key)
    await token.fetch_related('instance')

    return token.instance


@router.get("/", response_model=List[ModuleResponse])
async def get_registered():
    modules = await ModuleDB.all().prefetch_related('instances')

    module_responses = await ModuleResponse.module_response_from_db_model_list(
        modules
    )

    return module_responses


@router.post("/", response_model=ModuleResponse)
async def register(
        response: Response,
        name: str = Body(..., title='Module name', max_length=128, embed=True)
):
    module, created = await ModuleDB.get_or_create(name=name)

    await module.fetch_related('instances')

    module_response = await ModuleResponse.module_response_from_db_model(
        db_model=module
    )

    if created:
        response.status_code = status.HTTP_201_CREATED
    else:
        response.status_code = status.HTTP_200_OK

    return module_response


@router.post("/login", response_model=Token)
async def login(
        response: Response,
        request: Request,
        secret_key: str = Body(
            ...,
            title='Secret key of module for logging in',
            embed=True
        ),
        name: str = Body(
            ...,
            title='module_instance module name',
            embed=True
        ),
        instance: ModuleInstance = Depends(validate_login)

):
    module = await ModuleDB.get(secret_key=secret_key, name=name)
    instanceDB, _ = await ModuleInstanceDB.get_or_create(
        module=module,
        **instance.dict()
    )

    token = await TokenDB.create(
        instance=instanceDB
    )

    return token


@router.put("/{register_name}")
async def edit():
    pass


@router.post("/heartbeat", response_model=ModuleInstance)
async def heartbeat(
        instance: ModuleInstanceDB = Depends(authorize_instance)
):
    instance.status = ModuleInstance.UP
    await instance.save()

    return instance
