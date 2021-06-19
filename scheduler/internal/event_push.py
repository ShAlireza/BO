import json
import argparse

import pika

# TODO
#  1. log push errors or success with logger
#  2. ...

parser = argparse.ArgumentParser(
    prog='scheduler event pusher',
    description='push an event to queue',
    allow_abbrev=False
)

parser.add_argument(
    '-i',
    '--id',
    metavar='id',
    type=str,
    help='service cronjob id',
    required=True
)

parser.add_argument(
    '-t',
    '--tech',
    metavar='tech',
    type=str,
    help='service technology [e.g. mysql, postgres, ...]',
    required=True
)

parser.add_argument(
    '-m',
    '--mode',
    metavar='mode',
    type=str,
    help='event mode (backup, restore or validate)',
    required=True
)

parser.add_argument(
    '-H',
    '--host',
    metavar='host',
    type=str,
    help='service host',
    required=True
)

parser.add_argument(
    '-p',
    '--port',
    metavar='port',
    type=int,
    help='service port',
    required=True
)

parser.add_argument(
    '--rabbitmq-host',
    metavar='rabbitmq_host',
    type=str,
    help='rabbitmq host',
    required=True
)

parser.add_argument(
    '--rabbitmq-port',
    metavar='rabbitmq_port',
    type=str,
    help='rabbitmq port',
    required=True
)

parser.add_argument(
    '--namespace',
    metavar='namespace',
    type=str,
    help='job namespace',
    required=True
)

if __name__ == '__main__':
    args = parser.parse_args()

    push_data = {
        'id': args.id,
        'tech': args.tech,
        'mode': args.mode,
        'host': args.host,
        'port': args.port,
        'namespace': args.namespace
    }

    print(push_data)

    connection = pika.BlockingConnection(
        parameters=pika.ConnectionParameters(
            host=args.rabbitmq_host,
            port=args.rabbitmq_port
        )
    )

    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)

    channel.basic_publish(
        exchange='',
        routing_key=args.tech,
        body=json.dumps(push_data).encode('utf-8'),
        properties=pika.BasicProperties(
            delivery_mode=2  # make message persistent
        )
    )

    print(f' [x] Sent message: "{push_data}"')
    connection.close()


def get_parser():
    return parser
