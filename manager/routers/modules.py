from typing import Optional, List

import aiohttp
from aiohttp import ContentTypeError

from internal import KafkaHandler
from config import KAFKA_HOST, KAFKA_PORT

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
    Token as TokenDB,
    SecretKey as SecretKeyDB
)
from data.pydantic import (
    ModuleInstanceResponse,
    ModuleResponse,
    ModuleInstancePost,
    Token,
    LoginResponse,
    SecretKey
)

__all__ = ('router',)

# TODO
#  1. ...


router = APIRouter()


async def authorize_instance(
        authorization: str = Header('...', regex=r"^Bearer [a-zA-Z0-9]+$")
):
    token_key = authorization[7:]

    token = await TokenDB.get(key=token_key)
    await token.fetch_related('instance')

    return token.instance


async def get_kafka_handler():
    return KafkaHandler()


@router.get("/", response_model=List[ModuleResponse])
async def get_registered():
    modules = await ModuleDB.all().prefetch_related('instances')

    module_responses = await ModuleResponse.module_response_from_db_model_list(
        modules
    )

    return module_responses


@router.post("/", response_model=SecretKey)
async def register(
        response: Response,
):
    secret_key = await SecretKeyDB.create()

    return secret_key


@router.post("/login", response_model=LoginResponse)
async def login(
        response: Response,
        request: Request,
        secret_key: SecretKey = Body(
            ...,
            title='Secret key of module for logging in',
            embed=True
        ),
        name: str = Body(
            ...,
            title='module_instance module name',
            embed=True
        ),
        instance: ModuleInstancePost = Body(
            ...,
            title='Module instance body',
            embed=True
        ),
        kafka_handler: KafkaHandler = Depends(get_kafka_handler)
):
    await SecretKeyDB.get(secret_key=secret_key, valid=True)

    module, created = await ModuleDB.get_or_create(name=name)
    kafka_handler.create_topics(new_topics=[(name, 3, 1)])

    instanceDB, _ = await ModuleInstanceDB.get_or_create(
        module=module,
        **instance.dict()
    )

    token = await TokenDB.create(
        instance=instanceDB
    )

    return LoginResponse(
        token=token,
        kafka_host=KAFKA_HOST,
        kafka_port=KAFKA_PORT,
        kafka_topic=name
    )


@router.put("/{register_name}")
async def edit():
    pass


@router.post("/heartbeat", response_model=ModuleInstanceResponse)
async def heartbeat(
        instance: ModuleInstanceDB = Depends(authorize_instance)
):
    instance.status = ModuleInstanceDB.UP
    await instance.save()

    return instance
