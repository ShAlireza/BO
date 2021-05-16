from fastapi import FastAPI

from routers import scheduler_router

app = FastAPI()

app.include_router(
    scheduler_router,
    prefix='/api/scheduler',
    tags=['Scheduler']
)
