from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from prodamus import Prodamus

class ProdamusMiddleware(BaseMiddleware):
    def __init__(self,
                 prodamus: Prodamus) -> None:
        self.__prod = prodamus

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        data['prodamus'] = self.__prod
        return await handler(event, data)
    
