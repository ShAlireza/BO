from typing import List

from pydantic import BaseModel, Field

__all__ = ('TokenResponse', 'NameSpaceAdminResponse', 'NameSpacePost',
           'NameSpaceResponse')


class TokenBase(BaseModel):
    key: str = Field(
        ...,
        title='key of token',
        max_length=64
    )

    valid: bool = Field(
        ...,
        title='token validity'
    )


class NameSpaceBase(BaseModel):
    name: str = Field(
        ...,
        max_length=256,
        title='name of the namespace'
    )


class TokenResponse(TokenBase):
    id: int = Field(
        ...,
        title='token db id'
    )

    namespace: NameSpaceBase = Field(
        ...,
        title='namespaces of this token'
    )

    class Config:
        orm_mode = True


class NameSpacePost(NameSpaceBase):
    pass


class NameSpaceResponse(NameSpaceBase):
    id: int = Field(
        ...,
        title='namespace db id'
    )

    class Config:
        orm_mode = True


class NameSpaceAdminResponse(NameSpaceResponse):
    tokens: List[TokenBase] = Field(
        ...,
        title='tokens of this namespace'
    )

    @classmethod
    async def namespace_response_from_db_model(cls, db_model):
        return cls(
            id=db_model.id,
            name=db_model.name,
            tokens=await db_model.tokens.all()
        )

    @classmethod
    async def module_response_from_db_model_list(cls, db_models):
        namespace_responses = []

        for db_model in db_models:
            namespace_responses.append(
                await cls.namespace_response_from_db_model(db_model)
            )
        return namespace_responses

    class Config:
        orm_mode = True
