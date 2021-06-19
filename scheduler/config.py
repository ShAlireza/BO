import os
from tortoise import Tortoise

SCHEDULER_USER = os.getenv("SCHEDULER_USER")
PYTHONPATH = os.getenv("PYTHONPATH")
DATABASE_URL = os.getenv("DATABASE_URL")
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')
NAMESPACE_SERVER_HOST = os.getenv('NAMESPACE_SERVER_HOST')
NAMESPACE_SERVER_PORT = os.getenv('NAMESPACE_SERVER_PORT')
NAMESPACE_SERVER_URL = (
    f'http://'
    f'{NAMESPACE_SERVER_HOST}:'
    f'{NAMESPACE_SERVER_PORT}'
    f'/api/namespace/token/{{token_key}}'
)

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "scheduler": {
            "models": ["data.db.models", 'aerich.models'],
            "default_connection": "default",
        }
    }
}
