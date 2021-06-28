from typing import Optional, List

from internal import RabbitMQHandler
from exceptions import InvalidCredentialNames, ServiceInstanceExists
from config import (
    RABBITMQ_HOST,
    RABBITMQ_PORT,
    MINIO_ADDRESS,
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY
)

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

from bo_shared.utils.namespace import handle_namespace_token

from data.db import (
    Module as ModuleDB,
    ModuleInstance as ModuleInstanceDB,
    Token as TokenDB,
    SecretKey as SecretKeyDB,
    ServiceInstanceData as ServiceInstanceDataDB,
    ServiceInstanceCredential as ServiceInstanceCredentialDB
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
    ServiceInstanceCredential,
    ServiceInstanceDataPatch,
    ServiceInstanceDataResponse
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


@router.delete('/secret-key/{secret_key_id}', response_model=SecretKeyResponse)
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
        rabbitmq_queue=module.name,
        minio_address=MINIO_ADDRESS,
        minio_access_key=MINIO_ACCESS_KEY,
        minio_secret_key=MINIO_SECRET_KEY
    )


@router.get("/{module_name}",
            response_model=List[ServiceInstanceDataResponse])
async def get_service_instances_data(
        response: Response,
        namespace: str = Depends(handle_namespace_token),
        module_name: str = Path(
            ...,
            title='module name for adding service instance'
        )
):
    module = await ModuleDB.get(
        name=module_name
    )

    service_instances = await ServiceInstanceDataDB.filter(
        module=module,
        namespace=namespace
    ).prefetch_related('credentials')

    responses = await ServiceInstanceDataResponse.service_instance_response_from_db_model_list(
        service_instances
    )

    return responses


@router.post("/{module_name}/detail",
             response_model=ServiceInstanceDataResponse)
async def get_service_instance_data(
        namespace: str = Depends(handle_namespace_token),
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
    module = await ModuleDB.get(
        name=module_name
    )

    service_instance_data = await ServiceInstanceDataDB.get(
        module=module,
        host=host,
        port=port,
        namespace=namespace
    )

    await service_instance_data.fetch_related('credentials')

    response_data = await ServiceInstanceDataResponse.service_instance_response_from_db_model(
        service_instance_data
    )

    return response_data


@router.post("/{module_name}/exists")
async def service_exists(
        response: Response,
        namespace: str = Depends(handle_namespace_token),
        module_name: str = Path(
            ...,
            title='module name'
        ),
        host: str = Body(
            ...
        ),
        port: int = Body(
            ...
        )
):
    module = await ModuleDB.get(
        name=module_name
    )

    instance_exists = await ServiceInstanceDataDB.filter(
        module=module,
        host=host,
        port=port,
        namespace=namespace
    ).exists()

    print(instance_exists, module, host, port)

    if instance_exists:
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_404_NOT_FOUND


@router.post("/{module_name}", response_model=ServiceInstanceDataResponse)
async def add_service_instance_data(
        response: Response,
        namespace: str = Depends(handle_namespace_token),
        module_name: str = Path(
            ...,
            title='module name for adding service instance'
        ),
        service_instance: ServiceInstanceData = Body(
            ...,
            title='service instance data'
        )
):
    module = await ModuleDB.get(
        name=module_name
    )

    exists = await ServiceInstanceDataDB.filter(
        host=service_instance.host,
        port=service_instance.port,
        module=module,
        namespace=namespace
    ).exists()

    if exists:
        raise ServiceInstanceExists()

    service_instance_data = await ServiceInstanceDataDB.create(
        host=service_instance.host,
        port=service_instance.port,
        module=module,
        namespace=namespace
    )

    invalid_credentials = []

    for credential in service_instance.credentials:
        if not module.is_credential_valid(credential.name):
            invalid_credentials.append(credential.name)

    if invalid_credentials:
        raise InvalidCredentialNames(
            invalid_credentials=invalid_credentials,
            valid_credentials=module.valid_credential_names_list
        )

    for credential in service_instance.credentials:
        await ServiceInstanceCredentialDB.create(
            name=credential.name,
            value=credential.value,
            service_instance=service_instance_data
        )

    response_data = service_instance.dict()
    response_data['id'] = service_instance_data.id

    return response_data


@router.patch("/{module_name}/{service_instance_id}",
              response_model=ServiceInstanceDataResponse)
async def edit_service_instance_data(
        response: Response,
        namespace: str = Depends(handle_namespace_token),
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
    module = await ModuleDB.get(
        name=module_name
    )

    service_instance_data = await ServiceInstanceDataDB.get(
        id=service_instance_id,
        namespace=namespace
    )

    invalid_credentials = []

    for credential in service_instance.credentials:
        if not module.is_credential_valid(credential.name):
            invalid_credentials.append(credential.name)

    if invalid_credentials:
        raise InvalidCredentialNames(
            invalid_credentials=invalid_credentials,
            valid_credentials=module.valid_credential_names_list
        )

    if service_instance.credentials:
        await ServiceInstanceCredentialDB.filter(
            service_instance=service_instance_data
        ).delete()
        for credential in service_instance.credentials:
            await ServiceInstanceCredentialDB.create(
                name=credential.name,
                value=credential.value,
                service_instance=service_instance_data
            )

    update_data = service_instance.dict(exclude_unset=True)

    if 'credentials' in update_data:
        update_data.pop('credentials')

    await service_instance_data.update_from_dict(
        data=update_data
    )

    await service_instance_data.fetch_related('credentials')

    response_data = await ServiceInstanceDataResponse.service_instance_response_from_db_model(
        service_instance_data
    )

    return response_data


@router.delete("/{module_name}/{service_instance_id}",
               response_model=ServiceInstanceDataResponse)
async def delete_service_instance_data(
        response: Response,
        module_name: str = Path(
            ...,
            title='module name for adding service instance'
        ),
        namespace: str = Depends(handle_namespace_token),
        service_instance_id: int = Path(
            ...,
            title='service instance id',
            ge=0
        )
):
    service_instance_data = await ServiceInstanceDataDB.get(
        id=service_instance_id,
        namespace=namespace
    )

    await service_instance_data.fetch_related('credentials')

    response_data = await ServiceInstanceDataResponse.service_instance_response_from_db_model(
        service_instance_data
    )

    await ServiceInstanceDataDB.filter(
        id=service_instance_id,
        namespace=namespace
    ).delete()

    return response_data
