from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import User, Connection
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from messages.users import start_payment_message_2
from prodamus import Prodamus


async def newPrice(bot: Bot,
                   user: User,
                   connection: Connection,
                   prodamus: Prodamus):
    prices = await connection.getPaymentData
    payment_link = await prodamus.createLink(user,
                                             connection,
                                             2)
    payment_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Оплатить✅',
                                                                                 url=payment_link.payment_link)]])
    await bot.send_message(chat_id=user.user_id,
                           text=start_payment_message_2.format(price2=prices.price2),
                           reply_markup=payment_keyboard)
    await connection.updateLink(user,
                                payment_link=payment_link)

