import threading

from bo_shared.modules.interface import Consumer
from bo_shared.modules.app import create_module_app

from module import MySqlModule

import config

app = create_module_app()

consumer = Consumer(
    module_class=MySqlModule
)
consumer.start()
