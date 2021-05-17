from tortoise.models import Model
from tortoise import fields


class CronJobModel(Model):
    id = fields.UUIDField(pk=True)
    enable = fields.BooleanField(default=True)
    technology = fields.CharField(max_length=64)
    host = fields.CharField(max_length=128)
    port = fields.IntField(default=80)
    minute = fields.CharField(max_length=16, default='*')
    hour = fields.CharField(max_length=16, default='*')
    day_of_month = fields.CharField(max_length=16, default='*')
    month = fields.CharField(max_length=16, default='*')
    day_of_week = fields.CharField(max_length=16, default='*')

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    label = fields.CharField(max_length=128, null=True)
    full_command = fields.CharField(max_length=512, null=True)

    def __str__(self):
        return f'{self.technology}, {self.host}, {self.label}'
