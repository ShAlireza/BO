import requests

from fastapi import FastAPI

from routers import scheduler_router, manager_router, namespace_router

app = FastAPI()

app.include_router(
    scheduler_router,
    prefix='/api/scheduler',
    tags=['Scheduler']
)

app.include_router(
    manager_router,
    prefix='/api/manager',
    tags=['Manager']
)

app.include_router(
    namespace_router,
    prefix='/api/namespace',
    tags=['Namespace']
)
