from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from config import DATABASE_URL
from routers import service_router

app = FastAPI()

register_tortoise(
    app=app,
    db_url=DATABASE_URL,
    modules={'manager': ["data.db.models"]},
    generate_schemas=False,
    add_exception_handlers=True
)

app.include_router(
    service_router,
    prefix='/api/service',
    tags=['Service']
)