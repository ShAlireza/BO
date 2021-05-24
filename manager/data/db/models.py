from uuid import uuid4

from tortoise.models import Model
from tortoise import fields
from tortoise.validators import Validator
from tortoise.exceptions import ValidationError


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


class Module(Model):
    id = fields.CharField(
        max_length=48,
        pk=True,
        default=uuid4
    )

    name = fields.CharField(
        max_length=128,
        unique=True
    )

    secret_key = fields.CharField(
        max_length=128,
        unique=True
    )


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


class Token(Model):
    key = fields.CharField(
        max_length=64,
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
