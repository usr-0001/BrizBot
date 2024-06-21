from aiogram import Router

from .command_handler import router as command_handler_router

__all__ = ["router"]

# Router.
router = Router(name=__name__)
router.include_router(command_handler_router)
