from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from config import DATABASE_URL, MODULE_HEARTBEAT_INTERVAL

from routers import module_router

app = FastAPI()

app.include_router(
    module_router,
    prefix='/api/module',
    tags=['Service']
)

register_tortoise(
    app=app,
    db_url=DATABASE_URL,
    modules={'manager': ["data.db.models"]},
    generate_schemas=False,
    add_exception_handlers=True
)
