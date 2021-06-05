from bo_shared.modules.interface import Consumer
from bo_shared.modules.app import create_module_app

from module import MySqlModule

import config

app = create_module_app()

print('rabbitmq_host, rabbitmq_port, rabbitmq_queue')
print(config.RABBITMQ_HOST, config.RABBITMQ_PORT, config.RABBITMQ_QUEUE)


consumer = Consumer(
    module_class=MySqlModule
)

consumer()
