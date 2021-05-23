from pydantic import BaseModel, Field


class ModuleBase(BaseModel):
    name: str = Field(
        ...,
        title='Service name(mysql, postgres, git, ...)'
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


class ModuleResponse(ModuleBase):
    secret_key: str = Field(
        ...,
        title='Secret key for manager <-> module communication'
    )

    status: str = Field(
        'up',
        title='Module status(up, down)',
    )


class ModulePost(ModuleBase):
    pass
