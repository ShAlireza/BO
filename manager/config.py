import os
from tortoise import Tortoise

SCHEDULER_USER = os.getenv("SCHEDULER_USER")
PYTHONPATH = os.getenv("PYTHONPATH")
DATABASE_URL = os.getenv("DATABASE_URL")
TOKEN_EXPIRE_TIME = int(os.getenv('TOKEN_EXPIRE_TIME', 60 * 60 * 24))
MODULE_HEARTBEAT_INTERVAL = int(os.getenv('MODULE_HEARTBEAT_INTERVAL', 30))
KAFKA_HOST = os.getenv('KAFKA_HOST')
KAFKA_PORT = os.getenv('KAFKA_PORT')

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "manager": {
            "models": ["data.db.models", 'aerich.models'],
            "default_connection": "default",
        }
    }
}
