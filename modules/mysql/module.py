import json

from confluent_kafka import Consumer, KafkaException

from bo_shared.modules.interface import BaseModule
from minio import Minio

from config import KAFKA_HOST, KAFKA_PORT, KAFKA_TOPIC

mysql_dump = f'/usr/bin/mysqldump -u root'

conf = {'bootstrap.servers': f'{KAFKA_HOST}:{KAFKA_PORT}',
        'group.id': 0, 'auto.offset.reset': 'earliest',
        'session.timeout.ms': 6000}

consumer = Consumer(conf)


def print_assignment(consumer_, partitions):
    print('Assignment:', partitions)


consumer.subscribe([KAFKA_TOPIC], on_assign=print_assignment)


class MySqlModule(BaseModule):

    def __call__(self, *args, **kwargs):

        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            else:
                print(json.loads(msg.value().decode('utf-8')))

    def backup(self):
        pass

    def validate(self):
        pass

    def restore(self):
        pass


def main():
    client = Minio(
        "http://172.16.18.242:9000",
        access_key="minio",
        secret_key="minio123",
    )
    client.make_bucket()
