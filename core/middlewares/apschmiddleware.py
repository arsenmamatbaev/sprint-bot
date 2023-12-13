from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class SchedulerMiddleware(BaseMiddleware):
    def __init__(self,
                 scheduler: AsyncIOScheduler) -> None:
        self.__sched = scheduler

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        data['scheduler'] = self.__sched
        return await handler(event, data)
    