import os
from tortoise import Tortoise

SCHEDULER_USER = os.getenv("SCHEDULER_USER")
PYTHONPATH = os.getenv("PYTHONPATH")
DATABASE_URL = os.getenv("DATABASE_URL")
KAFKA_HOST = os.getenv('KAFKA_HOST')
KAFKA_PORT = os.getenv('KAFKA_PORT')

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "scheduler": {
            "models": ["data.db.models", 'aerich.models'],
            "default_connection": "default",
        }
    }
}
