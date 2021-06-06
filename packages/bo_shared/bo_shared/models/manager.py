from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

__all__ = (
    'ModuleInstanceBase', 'ModuleBase', 'ModuleResponse', 'Token',
    'ModuleInstanceResponse', 'ModuleInstancePost', 'LoginResponse',
    'SecretKey', 'SecretKeyResponse', 'ModulePost', 'ServiceInstanceData',
    'ServiceInstanceCredential', 'ServiceInstanceDataPatch',
    'ServiceInstanceDataResponse'
)


class ModuleInstanceBase(BaseModel):
    host: str = Field(
        ...,
        title='Instance host ip or domain',
        max_length=256
    )

    port: int = Field(
        ...,
        title='Instance port',
        ge=0
    )


class ModuleInstanceResponse(ModuleInstanceBase):
    state: str = Field(
        ...,
        title='Instance current state',
        max_length=64
    )

    created: datetime = Field(
        ...,
        title='Instance create time'
    )

    updated: datetime = Field(
        ...,
        title='Instance last update time'
    )


class ModuleInstancePost(ModuleInstanceBase):
    pass


class SecretKey(BaseModel):
    secret_key: str = Field(
        ...,
        max_length=128,
        title='Secret key for manager <-> module communication'
    )

    valid: bool = Field(
        default=True,
        title='Key is valid or not'
    )

    class Config:
        orm_mode = True


class SecretKeyResponse(SecretKey):
    id: int = Field(
        ...,
        title='id of secret key',
        ge=0
    )


class ModuleBase(BaseModel):
    name: str = Field(
        ...,
        title='Service name(mysql, postgres, git, ...)',
        max_length=128
    )

    valid_credential_names: str = Field(
        title='Valid credential names for this service'
    )


class ModulePost(ModuleBase):
    pass


class ModuleResponse(ModuleBase):
    id: str = Field(
        ...,
        title='Module db id',
        max_length=48
    )

    instances: List[ModuleInstanceResponse] = Field(
        title='Instances deployed of current module',
        default_factory=list
    )

    created: datetime = Field(
        ...,
        title='Module create time'
    )

    updated: datetime = Field(
        ...,
        title='Module last update time'
    )

    class Config:
        orm_mode = True

    @classmethod
    async def module_response_from_db_model(cls, db_model):
        return cls(
            id=db_model.id,
            name=db_model.name,
            instances=await db_model.instances.all(),
            valid_credential_names=db_model.valid_credential_names,
            created=db_model.created,
            updated=db_model.updated
        )

    @classmethod
    async def module_response_from_db_model_list(cls, db_models):
        module_responses = []

        for db_model in db_models:
            module_responses.append(
                await cls.module_response_from_db_model(db_model)
            )
        return module_responses


class Token(BaseModel):
    key: str = Field(
        ...,
        max_length=64,
        title='Token key value'
    )

    created: datetime = Field(
        ...,
        title='Token create time'
    )


class LoginResponse(BaseModel):
    token: Token = Field(
        ...,
        title='Token object'
    )

    rabbitmq_host: str = Field(
        ...,
        title='rabbitmq host'
    )

    rabbitmq_port: str = Field(
        ...,
        title='rabbitmq port'
    )

    rabbitmq_queue: str = Field(
        ...,
        title='module queue name in rabbitmq'
    )


class ServiceInstanceCredential(BaseModel):
    name: str = Field(
        ...,
        title='Credential name',
        max_length=256
    )

    value: str = Field(
        ...,
        title='Credential value',
        max_length=512
    )


class ServiceInstanceData(BaseModel):
    host: str = Field(
        ...,
        title='Instance host ip or domain',
        max_length=256
    )

    port: int = Field(
        ...,
        title='Instance port',
        ge=0
    )

    credentials: List[ServiceInstanceCredential] = Field(
        ...,
        title='credential list of this service instance'
    )

    class Config:
        orm_mode = True


class ServiceInstanceDataResponse(ServiceInstanceData):
    id: int = Field(
        ...,
        title='service instance db id',
        ge=0
    )

    @classmethod
    async def service_instance_response_from_db_model(cls, db_model):
        return cls(
            id=db_model.id,
            host=db_model.host,
            credentials=await db_model.credentials.all(),
            port=db_model.port
        )

    @classmethod
    async def service_instance_response_from_db_model_list(cls, db_models):
        responses = []

        for db_model in db_models:
            responses.append(
                await cls.service_instance_response_from_db_model(db_model)
            )
        return responses

    class Config:
        orm_mode = True


class ServiceInstanceDataPatch(BaseModel):
    host: Optional[str] = Field(
        None,
        title='Instance host ip or domain',
        max_length=256
    )

    port: Optional[int] = Field(
        None,
        title='Instance port',
        ge=0
    )

    credentials: Optional[List[ServiceInstanceCredential]] = Field(
        [],
        title='credential list of this service instance'
    )
