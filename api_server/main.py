import requests

from fastapi import FastAPI

from routers import scheduler_router

from internal.utils import generate_openapi_with_external_apis

app = FastAPI()

app.include_router(
    scheduler_router,
    prefix='/api/scheduler',
    tags=['Scheduler']
)
