import json
import argparse

from confluent_kafka import Producer

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
    '--kafka-host',
    metavar='kafka_host',
    type=str,
    help='kafka host',
    required=True
)

parser.add_argument(
    '--kafka-port',
    metavar='kafka_port',
    type=str,
    help='kafka port',
    required=True
)

if __name__ == '__main__':
    args = parser.parse_args()

    push_data = {
        'id': args.id,
        'tech': args.tech,
        'host': args.host,
        'port': args.port
    }

    print(push_data)

    conf = {'bootstrap.servers': f'{args.kafka_host}:{args.kafka_port}'}

    producer = Producer(**conf)


    def push_callback(error, message):
        if error:
            raise Exception(error)
        else:
            print(f'Messages delivered to {message.topic()}'
                  f' [{message.partition()}]'
                  f' @ {message.offset()}')


    try:
        producer.produce(
            args.tech,
            json.dumps(push_data).encode('utf-8'),
            callback=push_callback
        )
    except BufferError as e:
        raise e

    producer.poll(0)
    producer.flush()


def get_parser():
    return parser
