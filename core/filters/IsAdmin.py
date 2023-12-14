from typing import Any
from aiogram.types import Message
from aiogram.filters import BaseFilter
from database import Connection


class IsAdmin(BaseFilter):
    async def __call__(self, 
                       message: Message,
                       db: Connection) -> Any:
        admins = await db.getAdmins
        return message.from_user.id in admins

