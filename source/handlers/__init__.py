from aiogram import Router

from .command import router as command_handler_router
from .ibutton import router as inline_button_handler_router

__all__ = ["router"]

# Router.
router = Router(name=__name__)
router.include_router(command_handler_router)
router.include_router(inline_button_handler_router)
