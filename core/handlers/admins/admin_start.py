from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from ...keyboards.admins.inline import admin_menu
from messages.admins import first_message
from States import AdminsStates


async def start_admin(message: Message,
                      state: FSMContext):
    await message.answer(first_message,
                         reply_markup=admin_menu)
    await state.set_state(AdminsStates.main_menu)

