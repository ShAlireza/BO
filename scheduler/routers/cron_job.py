from fastapi import APIRouter, Depends

from internal.cron_job import CronHandler
from dependencies import get_cron_handler

router = APIRouter(
    prefix="/api/cron"
)

__all__ = ('router',)


@router.post("/")
async def add_job(
        cron_handler: CronHandler = Depends(get_cron_handler)
):
    pass


@router.get("/")
async def get_job(
        cron_handler: CronHandler = Depends(get_cron_handler)
):
    pass


@router.put("/")
async def edit_job(
        cron_handler: CronHandler = Depends(get_cron_handler)
):
    pass


@router.delete("/")
async def delete_job(
        cron_handler: CronHandler = Depends(get_cron_handler)
):
    pass
