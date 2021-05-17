from sqlalchemy import Column, DateTime, String, Integer, func, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class CronJobModel(Base):
    __tablename__ = 'scheduler.cronjob'

    id = Column(String, primary_key=True)
    enable = Column(Boolean, default=True)
    technology = Column(String)
    host = Column(String)
    port = Column(Integer)
    minute = Column(String)
    hour = Column(String)
    day_of_month = Column(String)
    month = Column(String)
    day_of_week = Column(String)
    created = Column(DateTime)

    label = Column(String, nullable=True)

