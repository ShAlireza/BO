from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .db import Base


class CronJob(Base):
    __tablename__ = 'cron_jobs'

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)

    enable = Column(Boolean, default=True)
