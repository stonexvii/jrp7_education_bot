from aiogram import Router

from .commands_handlers import command_router
from .callback_handlers import callback_router
from .fsm_handlers import fsm_router

main_router = Router()

main_router.include_routers(
    fsm_router,
    command_router,
    callback_router,
)

__all__ = [
    'main_router',
]
