from typing import List, Tuple

import pika

from config import RABBITMQ_HOST, RABBITMQ_PORT


class RabbitMQHandler:

    def __init__(self, rabbitmq_host=RABBITMQ_HOST,
                 rabbitmq_port=RABBITMQ_PORT):
        assert rabbitmq_host is not None, 'rabbitmq_host shouldn\'t be None'
        assert rabbitmq_port is not None, 'rabbitmq_port shouldn\'t be None'

        self.rabbitmq_host = rabbitmq_host
        self.rabbitmq_port = rabbitmq_port

    def create_queues(self, queue_names: List[str]):
        connection = self.new_connection()

        channel = connection.channel()
        channel.basic_qos(
            prefetch_count=1
        )

        for name in queue_names:
            channel.queue_declare(
                queue=name,
                durable=True
            )

        connection.close()

    def delete_queues(self, queue_names: List[str]):
        connection = self.new_connection()
        channel = connection.channel()

        for name in queue_names:
            channel.queue_delete(
                queue=name,
                if_unused=True
            )
        connection.close()

    def empty_queues_messages(self, queue_names: List[str]):
        connection = self.new_connection()
        channel = connection.channel()

        for name in queue_names:
            channel.queue_purge(
                queue=name
            )

        connection.close()

    def new_connection(self) -> pika.BlockingConnection:
        connection = pika.BlockingConnection(
            parameters=pika.ConnectionParameters(
                host=self.rabbitmq_host,
                port=self.rabbitmq_port
            )
        )

        return connection
