import abc
import json
from typing import Type

import pika
from minio import Minio


# Todo
#  1. Log errors and messages with logger
#  2. ...

class BaseModule(abc.ABC):

    def __init__(self):
        self.data = {}

    def __call__(self, data):
        self.data = data
        print(self.data)

        mode = self.data.get('mode')
        if mode == 'backup':
            self.backup()
        elif mode == 'validate':
            self.validate()
        elif mode == 'restore':
            self.restore()
        else:
            print(f'unexpected mode "{mode}"')

    def backup(self):
        raise NotImplementedError

    def restore(self):
        raise NotImplementedError

    def validate(self):
        raise NotImplementedError


class Consumer:

    def __init__(self, module_class: Type[BaseModule]):
        self.module_class = module_class

    def __call__(self):
        from config import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_QUEUE

        connection = pika.BlockingConnection(
            parameters=pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT
            )
        )

        def handle_message(ch, method, properties, body):
            data = json.loads(body.decode('utf-8'))

            print(f'started processing message: {data}')
            module = self.module_class()
            module(
                data=data
            )
            print(f'finished processing message: {data}')
            ch.basic_ack(
                delivery_tag=method.delivery_tag
            )

        channel = connection.channel()
        channel.basic_consume(
            queue=RABBITMQ_QUEUE,
            on_message_callback=handle_message
        )

        print(' [*] Waiting for messages.')
        channel.start_consuming()
