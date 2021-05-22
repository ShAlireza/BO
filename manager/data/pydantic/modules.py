from pydantic import BaseModel, Field


class Module(BaseModel):
    name: str = Field(
        ...,
        title='Service name(mysql, postgres, git, ...)'
    )

    secret_key: str = Field(
        ...,
        title='Secret key for manager <-> module communication'
    )

    host: str = Field(
        ...,
        title='Module host ip or domain'
    )

    port: int = Field(
        ...,
        title='Module port',
        ge=0
    )

    status: str = Field(
        'up',
        title='Module status(up, down)'
    )
