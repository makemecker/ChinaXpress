from .start import start_router
from .menu import menu_router
from .buy import buy_router
from .other import other_router
from aiogram import Router
from .pay import pay_router
from .delivery import delivery_router

router: Router = Router()
router.include_routers(start_router, menu_router, buy_router, pay_router, delivery_router, other_router)
