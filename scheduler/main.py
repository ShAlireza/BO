from fastapi import FastAPI

from routers import cron_job_router

app = FastAPI()

app.include_router(
    cron_job_router,
    tags=['Cron']
)
