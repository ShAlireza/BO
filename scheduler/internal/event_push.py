import argparse

parser = argparse.ArgumentParser(
    prog='scheduler event pusher',
    description='push an event to queue',
    allow_abbrev=False
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

args = parser.parse_args()

push_data = {
    'tech': args.tech,
    'host': args.host,
    'port': args.port
}

print(push_data)
