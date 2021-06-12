import os
from tortoise import Tortoise

AUTH_USER = os.getenv("AUTH_USER")
PYTHONPATH = os.getenv("PYTHONPATH")
DATABASE_URL = os.getenv("DATABASE_URL")

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "auth": {
            "models": ["data.db.models", 'aerich.models'],
            "default_connection": "default",
        }
    }
}
