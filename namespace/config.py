import os
from tortoise import Tortoise

NAMESPACE_USER = os.getenv("NAMESPACE_USER")
PYTHONPATH = os.getenv("PYTHONPATH")
DATABASE_URL = os.getenv("DATABASE_URL")

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "namespace": {
            "models": ["data.db.models", 'aerich.models'],
            "default_connection": "default",
        }
    }
}
