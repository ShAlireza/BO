import sys

from bo_shared.models.scheduler import (
    CronJob as CronJobShared,
    CronJobPost,
    CronJobResponse,
    CronJobPatch
)

from config import PYTHONPATH, RABBITMQ_HOST, RABBITMQ_PORT

__all__ = ('CronJob', 'CronJobPost', 'CronJobResponse', 'CronJobPatch')


class CronJob(CronJobShared):
    def generate_full_command(self):
        self.full_command = (f'{sys.executable} '
                             f'{PYTHONPATH}/internal/event_push.py '
                             f'--id {self.id} '
                             f'--tech {self.technology} '
                             f'--host {self.host} '
                             f'--port {self.port} '
                             f'--mode {self.mode} '
                             f'--rabbitmq-host {RABBITMQ_HOST} '
                             f'--rabbitmq-port {RABBITMQ_PORT} '
                             f'--namespace {self.namespace} ')
        return self.full_command
