from sqlalchemy.orm import Session

from . import models, schemas


def get_job(db: Session, job_id: str):
    return db.query(models.CronJob).filter(
        models.CronJob.job_id == job_id
    ).first()
