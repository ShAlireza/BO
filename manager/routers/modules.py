from typing import Optional, List

from fastapi import APIRouter, Path, Body, Query

__all__ = ('router',)

router = APIRouter()


@router.get("/")
async def get_registered():
    pass


@router.post("/")
async def register():
    pass


@router.put("/{register_name}")
async def edit():
    pass


@router.post("/heartbeat")
async def heartbeat():
    pass
