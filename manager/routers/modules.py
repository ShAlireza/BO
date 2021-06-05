from typing import Optional, List

import aiohttp
from aiohttp import ContentTypeError

from internal import KafkaHandler, RabbitMQHandler
from config import RABBITMQ_HOST, RABBITMQ_PORT

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
    SecretKey,
    SecretKeyResponse,
    ModulePost,
    ServiceInstanceData,
    ServiceInstanceCredential
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


async def get_rabbitmq_handler():
    return RabbitMQHandler()


@router.get("/", response_model=List[ModuleResponse])
async def get_registered():
    modules = await ModuleDB.all().prefetch_related('instances')

    module_responses = await ModuleResponse.module_response_from_db_model_list(
        modules
    )

    return module_responses


@router.post("/secret-key", response_model=SecretKeyResponse)
async def create_secret_key(
        response: Response,
):
    secret_key = await SecretKeyDB.create()

    return secret_key


@router.get("/secret-key", response_model=List[SecretKeyResponse])
async def get_secret_keys(
        response: Response,
):
    secret_keys = await SecretKeyDB.all()

    return secret_keys


@router.patch("/secret-key/{secret_key_id}", response_model=SecretKeyResponse)
async def toggle_secret_key_validity(
        response: Response,
        secret_key_id: int = Path(..., title='id of secret_key', ge=0)
):
    secret_key = await SecretKeyDB.get(id=secret_key_id)

    secret_key.valid = not secret_key.valid

    await secret_key.save()

    return secret_key


@router.delete('secret-key/{secret_key_id}', response_model=SecretKeyResponse)
async def delete_secret_key(
        response: Response,
        secret_key_id: int = Path(..., title='id of secret_key', ge=0)
):
    secret_key = await SecretKeyDB.get(id=secret_key_id)

    await SecretKeyDB.filter(id=secret_key_id).delete()

    return secret_key


@router.post("/login", response_model=LoginResponse)
async def login(
        secret_key: str = Body(
            ...,
            title='Secret key of module for logging in',
            embed=True
        ),
        module: ModulePost = Body(
            ...,
            title='module_instance module initial data',
            embed=True
        ),
        instance: ModuleInstancePost = Body(
            ...,
            title='Module instance body',
            embed=True
        ),
        rabbitmq_handler: RabbitMQHandler = Depends(get_rabbitmq_handler)
):
    await SecretKeyDB.get(secret_key=secret_key, valid=True)

    module_db, created = await ModuleDB.get_or_create(
        name=module.name,
        valid_credential_names=module.valid_credential_names
    )
    await module_db.save()

    rabbitmq_handler.create_queues(
        queue_names=[module.name]
    )

    instance_db, _ = await ModuleInstanceDB.get_or_create(
        module=module_db,
        **instance.dict()
    )

    token = await TokenDB.create(
        instance=instance_db
    )

    return LoginResponse(
        token=token,
        rabbitmq_host=RABBITMQ_HOST,
        rabbitmq_port=RABBITMQ_PORT,
        rabbitmq_queue=module.name
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
