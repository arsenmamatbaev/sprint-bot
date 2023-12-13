from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from database import Connection

class DbMiddleware(BaseMiddleware):
    def __init__(self,
                 connection: Connection) -> None:
        self.__conn = connection

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        data['db'] = self.__conn
        return await handler(event, data)
    
