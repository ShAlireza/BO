from sqlalchemy.orm import Session

from . import models, schemas


def get_job(db: Session, job_id: int):
    return db.query(models.CronJob).filter(
        models.CronJob.id == job_id
    ).first()


def create_job(db: Session, cron_job: schemas.CronJob):
    pass
