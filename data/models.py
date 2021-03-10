from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .db import Base


class CronJob(Base):
    __tablename__ = 'cron_jobs'

    id = Column(Integer, primary_key=True, index=True)
    enable = Column(Boolean, default=True)
    technology = Column(String(128))
    arguments = relationship("Argument", back_populates="cron_job")


class Argument(Base):
    __tablename__ = 'arguments'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128))
    value = Column(String(256))

    cron_job_id = Column(Integer, ForeignKey("cron_jobs.id"))
    cron_job = relationship("CronJob", back_populates="arguments")
