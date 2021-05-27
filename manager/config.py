import os
from tortoise import Tortoise

SCHEDULER_USER = os.getenv("SCHEDULER_USER")
PYTHONPATH = os.getenv("PYTHONPATH")
DATABASE_URL = os.getenv("DATABASE_URL")
TOKEN_EXPIRE_TIME = int(os.getenv('TOKEN_EXPIRE_TIME', 60 * 60 * 24))
MODULE_DOWN_TIMEOUT = int(os.getenv('MODULE_DOWN_TIMEOUT', 60 * 60))
KAFKA_HOST = os.getenv('KAFKA_HOST')
KAFKA_PORT = os.getenv('KAFKA_PORT')

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "manager": {
            "models": ["data.db.models", 'aerich.models'],
            "default_connection": "default",
        }
    }
}
