from uuid import uuid4

from tortoise.models import Model
from tortoise import fields

from bo_shared.utils import generate_token_key

__all__ = ('NameSpace', 'Token')


class NameSpace(Model):
    name = fields.CharField(
        max_length=256,
        unique=True
    )

    class Meta:
        table = 'namespace.namespace'


class Token(Model):
    key = fields.CharField(
        max_length=64,
        default=lambda: generate_token_key(32)
    )

    namespace = fields.ForeignKeyField(
        'namespace.NameSpace',
        related_name='tokens',
        on_delete=fields.CASCADE
    )

    valid = fields.BooleanField(
        default=True
    )

    class Meta:
        table = 'namespace.token'
