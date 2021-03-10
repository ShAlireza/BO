from typing import List, Optional

from fastapi import APIRouter

from data import crud, models, schemas
from data.db import SessionLocal, engine

router = APIRouter(
    prefix="/api/cron"
)

__all__ = ('router',)


@router.post("/")
def add_job():
    pass


@router.get("/")
def get_job():
    pass
