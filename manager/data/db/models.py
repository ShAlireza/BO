from uuid import uuid4

from tortoise.models import Model
from tortoise import fields
from tortoise.validators import Validator
from tortoise.exceptions import ValidationError

from bo_shared.utils import generate_token_key, generate_secret_key

from config import TOKEN_EXPIRE_TIME

__all__ = ('Module', 'ModuleInstance', 'Token',
           'SecretKey', 'ServiceInstanceData', 'ServiceInstanceCredential')


# Todo
#  1. Module -> ServiceHandler, ModuleInstance -> ServiceHandlerInstance
#  2. ...


class NoneNegativeValidator(Validator):
    """
    A validator to validate the non-negative integer
    """

    def __init__(self, min_length: int):
        self.min_length = min_length

    def __call__(self, value: int):
        if value is None:
            raise ValidationError("Value must not be None")
        if value < 0:
            raise ValidationError(f"Value '{value}' must be non-negative")


class SecretKey(Model):
    secret_key = fields.CharField(
        max_length=128,
        unique=True,
        default=lambda: generate_secret_key(length=64)
    )

    valid = fields.BooleanField(
        default=True
    )


class Module(Model):
    id = fields.CharField(
        max_length=48,
        pk=True,
        default=lambda: str(uuid4())
    )

    name = fields.CharField(
        max_length=128,
        unique=True
    )

    created = fields.DatetimeField(
        auto_now_add=True
    )

    updated = fields.DatetimeField(
        auto_now=True
    )

    valid_credential_names = fields.TextField(
        description='a comma separated set of values that are valid for this '
                    'service credentials names'
    )

    @classmethod
    async def is_unique(cls, name):
        exists = await cls.filter(name=name).exists()

        return exists

    @property
    def valid_credential_names_list(self):
        import re

        return re.split('\\s*,\\s*', self.valid_credential_names)

    def is_credential_valid(self, credential_name):
        return credential_name in self.valid_credential_names_list


class ModuleInstance(Model):
    UP = 'up'
    DOWN = 'down'

    module = fields.ForeignKeyField(
        model_name='manager.Module',
        related_name='instances',
        on_delete=fields.CASCADE
    )

    host = fields.CharField(
        max_length=256
    )

    port = fields.IntField(
        validators=[NoneNegativeValidator]
    )

    state = fields.CharField(
        max_length=64,
        default=DOWN
    )

    created = fields.DatetimeField(
        auto_now_add=True
    )

    updated = fields.DatetimeField(
        auto_now=True
    )


class ServiceInstanceData(Model):
    host = fields.CharField(
        max_length=256
    )

    port = fields.IntField(
        validators=[NoneNegativeValidator]
    )

    module = fields.ForeignKeyField(
        model_name='manager.Module',
        related_name='service_instances',
        on_delete=fields.CASCADE
    )


class ServiceInstanceCredential(Model):
    name = fields.CharField(
        max_length=256
    )

    value = fields.CharField(
        max_length=512
    )

    service_instance = fields.ForeignKeyField(
        model_name='manager.ServiceInstanceData',
        related_name='credentials',
        on_delete=fields.CASCADE
    )


class Token(Model):
    EXPIRE_TIME = TOKEN_EXPIRE_TIME

    key = fields.CharField(
        max_length=64,
        default=lambda: generate_token_key(length=24),
        unique=True
    )

    instance = fields.ForeignKeyField(
        model_name='manager.ModuleInstance',
        related_name='tokens',
        on_delete=fields.CASCADE
    )

    created = fields.DatetimeField(
        auto_now_add=True
    )

    expired = fields.BooleanField(
        default=False
    )

    @property
    def is_valid(self):
        return not self.expired
