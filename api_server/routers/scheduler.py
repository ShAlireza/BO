from typing import Optional, List

from fastapi import APIRouter

__all__ = ('router',)

router = APIRouter()


@router.get("/{product_name}")
def get_jobs():
    pass


@router.get("/")
def get_jobs_by_product():
    pass
