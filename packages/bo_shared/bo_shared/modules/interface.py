import threading
import abc
import json
import requests
from typing import Type
import subprocess

import pika
import aiohttp
from minio import Minio

from config import MANAGER_HOST, MANAGER_PORT, MINIO_CLIENT


# Todo
#  1. Log errors and messages with logger
#  2. ...

class BaseModule(abc.ABC):

    def __init__(self):
        self.raw_data = {}
        self.flat_data = {}

    def __call__(self, data):
        self.raw_data = self._get_raw_data_from_manager(data)
        self.flat_data = self._get_flat_data(self.raw_data)

        print(self.raw_data, self.flat_data)

        mode = self.raw_data.get('mode')

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

    def create_necessary_bucket_minio(self, label, module):
        process = subprocess.run(
            [MINIO_CLIENT, 'mb', f'storage/backups/{label}/{module}']
        )

        return f'storage/backups/{label}/{module}' if process.returncode == 0 \
            else None

    def _get_raw_data_from_manager(self, data):
        module_name = data.get('tech')
        host = data.get('host')
        port = data.get('port')
        url = f'http://{MANAGER_HOST}:{MANAGER_PORT}/api/module/{module_name}/detail'

        response = requests.post(
            url=url,
            json={
                'host': host,
                'port': port
            }
        )

        raw_data = None
        try:
            raw_data = response.json()
        except ValueError as e:
            print(e)

        raw_data['mode'] = data.get('mode')
        raw_data['tech'] = module_name
        raw_data['module'] = module_name
        raw_data['label'] = data.get('label')

        return raw_data

    def _get_flat_data(self, raw_data):
        flat_data = raw_data.copy()
        for credential in raw_data.get('credentials'):
            flat_data[credential.get('name')] = credential.get('value')

        flat_data.pop('credentials')

        return flat_data


class Consumer(threading.Thread):

    def __init__(self, module_class: Type[BaseModule]):
        super().__init__(daemon=True)
        self.module_class = module_class

    def run(self):
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
