from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from routers import auth_router

from config import DATABASE_URL

app = FastAPI()

register_tortoise(
    app=app,
    db_url=DATABASE_URL,
    modules={'auth': ["data.db.models"]},
    generate_schemas=False,
    add_exception_handlers=True
)

app.include_router(
    auth_router,
    prefix='/api/auth',
    tags=['Auth']
)
