import uuid
from datetime import datetime
from typing import List, Optional, Union, Any
from uuid import UUID

from pydantic import BaseModel, Field, validator, ValidationError

from bo_shared.models.scheduler import (
    CronJob as CronJobShared,
    CronJobPost,
    CronJobResponse,
    CronJobPatch
)

from config import PYTHONPATH, KAFKA_HOST, KAFKA_PORT

__all__ = ('CronJob', 'CronJobPost', 'CronJobResponse', 'CronJobPatch')


class CronJob(CronJobShared):
    def generate_full_command(self):
        self.full_command = (f'python {PYTHONPATH}/internal/event_push.py '
                             f'--id {self.id} '
                             f'--tech {self.technology} '
                             f'--host {self.host} '
                             f'--port {self.port} '
                             f'--mode {self.mode} '
                             f'--kafka-host {KAFKA_HOST} '
                             f'--kafka-port {KAFKA_PORT}')
        return self.full_command
