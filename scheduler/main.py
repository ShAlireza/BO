from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise


from routers import cron_job_router
from internal.cron_handler import CronHandler
from data.db.models import CronJobModel
from data.pydantic.models import CronJob

from config import SCHEDULER_USER
from config import DATABASE_URL

app = FastAPI()

register_tortoise(
    app=app,
    db_url=DATABASE_URL,
    modules={'scheduler': ["data.db.models"]},
    generate_schemas=False,
    add_exception_handlers=True
)

app.include_router(
    cron_job_router,
    prefix='/api/cron',
    tags=['Cron']
)


@app.on_event('startup')
async def init_cron_jobs():
    cron_jobs = await CronJobModel.all()
    cron_handler = CronHandler(
        user=SCHEDULER_USER
    )
    for cron_job in cron_jobs:
        cron_job_object = CronJob.instance_from_tortoise_model(cron_job)
        if not cron_handler.job_exists(
                job_id=cron_job.id
        ):
            cron_job_object.generate_full_command()
            cron_handler.add_job(
                cron_job=cron_job_object
            )
