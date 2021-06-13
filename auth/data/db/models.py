from uuid import uuid4

from tortoise.models import Model
from tortoise import fields

from bo_shared.utils import generate_token_key


class NameSpace(Model):
    name = fields.CharField(
        max_length=256,
        unique=True
    )


class Token(Model):
    key = fields.CharField(
        max_length=64,
        default=lambda: generate_token_key(32)
    )

    namespaces = fields.ManyToManyField(
        'auth.NameSpace',
        related_name='tokens',
        on_delete=fields.CASCADE
    )

    valid = fields.BooleanField(
        default=True
    )
