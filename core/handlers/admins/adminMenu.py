from aiogram import Bot
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.fsm.context import FSMContext
from messages.admins import first_message
from ...keyboards.admins.inline import admin_menu, cancel_keyboard
from ...keyboards.admins.reply import chooseUser
from States import AdminsStates
from database import Connection, User
import pandas as pd
import os


async def toMainMenu(message: Message,
                     state: FSMContext):
    await message.answer(first_message,
                         reply_markup=admin_menu)
    await state.set_state(AdminsStates.main_menu)
        

# ---------------------- Управление оплатой ----------------------

async def editPricesHandler(call: CallbackQuery,
                            state: FSMContext):
    await call.message.delete()
    await call.message.answer("Пришлите новые цены в формате:\nprice1(цена со скидкой),price2(цена без скидки)\nПример: 1990,2500",
                              reply_markup=cancel_keyboard)
    await state.set_state(AdminsStates.editPrice)


async def newPricesEdit(message: Message, 
                        state: FSMContext,
                        db: Connection):
    prices = message.text.split(',')
    await db.updatePrices(int(prices[0]),
                          int(prices[1]))
    await message.answer("Изменения прошли успешно!")
    await toMainMenu(message=message,
                     state=state)


# ----------------------------------------------------------------


# ------------- Получени списка пользователей(Excel) ----------------

async def getUserListExcel(call: CallbackQuery,
                           db: Connection):
    usersId = []
    fullNames = []
    userNames = []
    levels = []
    paymentLinks = []
    registerDates = []
    path = os.path.dirname(os.path.abspath(__file__))
    users = await db.getUsers
    for user in users:
        usersId.append(user.user_id)
        fullNames.append(user.full_name)
        userNames.append(user.username)
        levels.append(user.level)
        paymentLinks.append(user.payment_link)
        registerDates.append(user.register_date)
    frame = pd.DataFrame({
        "ID Пользователя": usersId,
        "Имя пользователя": fullNames,
        "@username": userNames,
        "Статус": levels,
        "Платежная ссылка": paymentLinks,
        "Время регистрации(мск)": registerDates 
    })
    frame.to_excel(path + '\\users.xlsx')
    filesToSend = FSInputFile(path + "\\users.xlsx")
    await call.message.answer_document(filesToSend)
    os.remove(path + '\\users.xlsx')


# -------------------------------------------------------------------

async def toManiMenuHandler(call: CallbackQuery,
                            state: FSMContext):
    await call.message.delete()
    await call.message.answer(first_message,
                              reply_markup=admin_menu)
    await state.set_state(AdminsStates.main_menu)



async def doMailing(call: CallbackQuery,
                    state: FSMContext):
    await call.message.answer("Пришлите файл рассылки",
                              reply_markup=cancel_keyboard)
    await state.set_state(AdminsStates.mailing_file_state)


async def mailing_file(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data({"file_type": "photo", "file_id": message.photo[-1].file_id})
    elif message.video:
        await state.update_data({"file_type": "video", "file_id": message.video.file_id})
    elif message.document:
        await state.update_data({"file_type": "document", "file_id": message.document.file_id})
    else:
        await message.answer('Видео или фото!',
                             reply_markup=cancel_keyboard)
        return
    await message.answer('Теперь пришлите текст рассылки',
                         reply_markup=cancel_keyboard)
    await state.set_state(AdminsStates.mailing_text_state)


async def mailing_text(message: Message, 
                       state: FSMContext, 
                       db: Connection,
                       bot: Bot):
    await message.answer('Начинаю операцию рассылки, она может занять до 5 минут, ожидайте...')
    users = await db.getUsers
    data = await state.get_data()
    send_user = 0
    if data['file_type'] == 'photo':
        for user in users:
            try:
                await bot.send_photo(chat_id=user.user_id,
                                     photo=data['file_id'],
                                     caption=message.text)
                send_user += 1
            except Exception as e:
                send_user -= 1
    elif data['file_type'] == 'video':
        for user in users:
            try:
                await bot.send_video(chat_id=user.user_id,
                                     video=data['file_id'],
                                     caption=message.text)
                send_user += 1
            except Exception as e:
                send_user -= 1
    elif data['file_type'] == 'document':
        for user in users:
            try:
                await bot.send_document(chat_id=user.user_id,
                                        document=data['file_id'],
                                        caption=message.text)
                send_user += 1
            except Exception as e:
                send_user -= 1
    await bot.send_message(chat_id=-4086012311,
                           text=f'Была произведена рассылка\nКолличество получателей: {send_user}')
    await message.answer('Рассылка завершена, подробности в группах с отчетами!')

    await toMainMenu(message, state)
