from typing import List, Optional

from fastapi import APIRouter

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
