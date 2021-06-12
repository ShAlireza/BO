from uuid import uuid4

from tortoise.models import Model
from tortoise import fields


class CronJobModel(Model):
    id = fields.CharField(max_length=48, pk=True, default=uuid4)

    enable = fields.BooleanField(default=True)
    technology = fields.CharField(max_length=64)
    mode = fields.CharField(max_length=32)

    host = fields.CharField(max_length=128)
    port = fields.IntField(default=80)
    minute = fields.CharField(max_length=16, default='*')
    hour = fields.CharField(max_length=16, default='*')
    day_of_month = fields.CharField(max_length=16, default='*')
    month = fields.CharField(max_length=16, default='*')
    day_of_week = fields.CharField(max_length=16, default='*')

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    namespace = fields.CharField(max_length=128, null=True)
    full_command = fields.CharField(max_length=512, null=True)

    def __str__(self):
        return f'{self.technology}, {self.host}, {self.namespace}'
