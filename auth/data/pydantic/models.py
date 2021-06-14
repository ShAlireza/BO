from typing import List

from pydantic import BaseModel, Field


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


class TokenResponse(TokenBase):
    id: int = Field(
        ...,
        title='token db id'
    )

    namespace: 'NameSpaceBase' = Field(
        ...,
        title='namespaces of this token'
    )


class NameSpaceBase(BaseModel):
    name: str = Field(
        ...,
        max_length=256,
        title='name of the namespace'
    )


class NameSpaceResponse(NameSpaceBase):
    tokens: List[TokenBase] = Field(
        ...,
        title='tokens of this namespace'
    )
