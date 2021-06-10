import threading

from bo_shared.modules.interface import Consumer
from bo_shared.modules.app import create_module_app

from module import MySqlModule

import config

app = create_module_app()

print(config.RABBITMQ_HOST, config.RABBITMQ_PORT, config.RABBITMQ_QUEUE,
      config.MINIO_ADDRESS, config.MINIO_ACCESS_KEY, config.MINIO_SECRET_KEY)

consumer = Consumer(
    module_class=MySqlModule
)
consumer.start()
