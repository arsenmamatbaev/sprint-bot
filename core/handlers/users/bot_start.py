from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database import Connection, User
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from prodamus import Prodamus
from messages.users import start_payment_message_1


async def start(message: Message,
                db: Connection,
                scheduler: AsyncIOScheduler,
                prodamus: Prodamus):
    user = User(user_id=message.from_user.id,
                full_name=message.from_user.full_name,
                username=message.from_user.username)
    exist = await db.userExist(user)
    prices = await db.getPaymentData
    if not exist:
        payment_link = await prodamus.createLink(user,
                                                 db)
        payment_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Оплатить✅',
                                                                                       url=payment_link.payment_link)]])
        await message.answer(start_payment_message_1.format(payment_link=payment_link.payment_link,
                                                            price1=prices.price1,
                                                            price2=prices.price2,
                                                            expire=prices.expire),
                                                            reply_markup=payment_keyboard)
        await db.create_or_update(user,
                                  payment_link=payment_link)
    else:
        payment_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Оплатить✅',
                                                                                       url=exist.payment_link)]])
        await message.answer(start_payment_message_1.format(payment_link=exist.payment_link,
                                                            price1=prices.price1,
                                                            price2=prices.price2,
                                                            expire=prices.expire),
                                                            reply_markup=payment_keyboard)

