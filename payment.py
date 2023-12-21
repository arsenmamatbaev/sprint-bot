import os
from aiogram import Dispatcher
from flask import Flask, request, Response
from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from dotenv.main import load_dotenv
from core.keyboards.users.inline import anketa_mentorstvo_keyboard, get_keyboard
from messages import users as msg
from messages.admins import payment_message
import Files 
import asyncio


app = Flask(__name__)


load_dotenv()

bot = Bot(os.getenv('API_KEY'),
          protect_content=True)
event_loop = asyncio.get_event_loop()


async def SendFirstLesson(user_id: int,
                          phone: str,
                          email: str,
                          sum: str):
    await bot.send_message(chat_id=os.getenv('ADMIN_CHAT'),
                           text=payment_message.format(user_id=user_id,
                                                       phone_number=phone,
                                                       email=email,
                                                       sum=sum))
    await bot.send_video(chat_id=user_id,
                         video=Files.lesson_1,
                         caption=msg.lesson_1_caption)
    await bot.send_message(chat_id=user_id,
                           text=msg.anketa_mentorstvo_text,
                           reply_markup=anketa_mentorstvo_keyboard)
    await bot.send_message(chat_id=user_id,
                           text=msg.subscribe_tg)
    await bot.send_message(chat_id=user_id,
                           text='Лови бонусный файл про создание продающего визуала в блоге🎁',
                           reply_markup=get_keyboard)


@app.route('/payment')
def newPayment():
    data = request.values.to_dict()
    if data['payment_status'] == 'success':
        try:
            event_loop.run_until_complete(SendFirstLesson(user_id=int(data['order_id']),
                                                          phone=data['customer_phone'],
                                                          email=data['customer_email'],
                                                          sum=data['payment_sum']))
        except Exception as e:
            print(e)
            return Response('Возникла какая-то ошибка в процессе обработки платежа',
                            status=405)
    else:
        return Response("Status is not 'succes'",
                        status=400)

