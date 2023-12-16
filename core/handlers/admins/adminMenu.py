from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from messages.admins import first_message
from ...keyboards.admins.inline import admins_settings_keyboard,admin_menu
from ...keyboards.admins.reply import chooseUser
from States import AdminsStates
from database import Connection, User


async def toMainMenu(message: Message,
                     state: FSMContext):
    await message.answer(first_message,
                         reply_markup=admin_menu)
    await state.set_state(AdminsStates.main_menu)


async def main_menu_handler(call: CallbackQuery,
                            state: FSMContext):
    await call.answer()
    await call.message.delete()
    if call.data == 'admin_settings':
        await call.message.answer('<b>Выберите действие:</b>',
                                  reply_markup=admins_settings_keyboard)
        await state.set_state(AdminsStates.admin_settings_menu)
        

# ------------- Управлениями админами ----------------

async def add_admin(call: CallbackQuery,
                    state: FSMContext):
    await call.message.delete()
    if call.data == 'admin_add':
        await call.message.answer('Выберите пользователя',
                                  reply_markup=chooseUser)
        await state.set_state(AdminsStates.choose_user_menu)

    
async def choose_user_handler(message: Message,
                              db: Connection,
                              state: FSMContext):
    if message.text == 'Отмена':
        return await toMainMenu(message=message,
                          state=state)
    if not message.user_shared:
        await message.answer("Пожалуйста отправьте мне пользвателя нажав на клавиатуру ниже",
                             reply_markup=chooseUser)
        return
    await db.addAdmin(message.user_shared.user_id)
    await message.answer("🌟Админ успешно добавлен в базу")
    await toMainMenu(message=message,
                     state=state)

# ----------------------------------------------------



async def toManiMenuHandler(call: CallbackQuery,
                            state: FSMContext):
    await call.message.delete()
    await call.message.answer(first_message,
                              reply_markup=admin_menu)
    await state.set_state(AdminsStates.main_menu)

