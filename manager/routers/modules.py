from typing import Optional, List

from fastapi import APIRouter, Path, Body, Query, Response, status

from data.db import (
    Module as ModuleDB,
    ModuleInstance as ModuleInstanceDB,
    Token as TokenDB
)
from data.pydantic import (
    ModuleInstance,
    ModuleResponse
)

__all__ = ('router',)

router = APIRouter()


@router.get("/", response_model=List[ModuleResponse])
async def get_registered():
    modules = await ModuleDB.all().prefetch_related('instances')

    module_responses = await ModuleResponse.module_response_from_db_model_list(
        modules
    )

    return module_responses


@router.post("/", response_model=ModuleResponse)
async def register(
        response: Response,
        name: str = Body(..., title='Module name', max_length=128, embed=True)
):
    module, created = await ModuleDB.get_or_create(name=name)

    await module.fetch_related('instances')

    module_response = await ModuleResponse.module_response_from_db_model(
        db_model=module
    )

    if created:
        response.status_code = status.HTTP_201_CREATED
    else:
        response.status_code = status.HTTP_200_OK

    return module_response


@router.post("/login")
async def login():
    pass


@router.put("/{register_name}")
async def edit():
    pass


@router.post("/heartbeat")
async def heartbeat():
    pass
