from fastapi import FastAPI

from scheduler.routers import cron_job_router

app = FastAPI()

app.include_router(
    cron_job_router,
    tags=['cron']
)
