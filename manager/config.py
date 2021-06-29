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
MINIO_ADDRESS = os.getenv('MINIO_ADDRESS')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')

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
        "manager": {
            "models": ["data.db.models", 'aerich.models'],
            "default_connection": "default",
        }
    }
}
