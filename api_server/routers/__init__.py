from .scheduler import router as scheduler_router
from .manager import router as manager_router
from .namespace import router as namespace_router

__all__ = ('scheduler_router', 'manager_router','namespace_router')
