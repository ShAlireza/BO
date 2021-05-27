from uuid import uuid4
import secrets
import string

from tortoise.models import Model
from tortoise import fields
from tortoise.validators import Validator
from tortoise.exceptions import ValidationError

from config import TOKEN_EXPIRE_TIME

__all__ = ('generate_secret_key', 'Module', 'ModuleInstance', 'Token')


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


def generate_secret_key(length=64):
    chars = string.ascii_letters + string.digits + "@$#!.<=>+-_?*%"
    key = ''.join(secrets.choice(chars) for _ in range(length))

    return key


def generate_token_key(length=64):
    return secrets.token_hex(length)


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

    secret_key = fields.CharField(
        max_length=128,
        unique=True,
        default=lambda: generate_secret_key(length=64)
    )

    created = fields.DatetimeField(
        auto_now_add=True
    )

    updated = fields.DatetimeField(
        auto_now=True
    )

    @classmethod
    async def is_unique(cls, name):
        exists = await cls.filter(name=name).exists()

        return exists


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
