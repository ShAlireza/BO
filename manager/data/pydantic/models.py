from pydantic import BaseModel, Field


class ModuleInstance(BaseModel):
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

    state: str = Field(
        'down',
        title='Instance current state',
        max_length=64
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

    instances: ModuleInstance = Field(
        ...,
        title='Instances deployed of current module'
    )
