from typing import List, Optional

from fastapi import APIRouter, Body, Path, Query

router = APIRouter()


@router.get('/token/namespace')
def get_namespace():
    pass


@router.get('/namespace')
def get_namespaces():
    pass


@router.post('/namespace')
def create_namespace():
    pass


@router.delete('/namespace/{namespace_name')
def delete_namespace():
    pass


@router.patch('/namespace/{namespace_name}')
def edit_namespace():
    pass


@router.post('/token')
def create_token():
    pass


@router.patch('/token/{token_id}')
def toggle_token_validity():
    pass


@router.delete('/token/{token_id}')
def delete_token():
    pass
