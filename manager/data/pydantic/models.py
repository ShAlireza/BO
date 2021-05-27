from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

__all__ = (
    'ModuleInstanceBase', 'ModuleBase', 'ModuleResponse', 'Token',
    'ModuleInstanceResponse'
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


class ModuleBase(BaseModel):
    name: str = Field(
        ...,
        title='Service name(mysql, postgres, git, ...)',
        max_length=128
    )

    secret_key: str = Field(
        ...,
        max_length=128,
        title='Secret key for manager <-> module communication'
    )


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
            secret_key=db_model.secret_key,
            instances=await db_model.instances.all()
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
