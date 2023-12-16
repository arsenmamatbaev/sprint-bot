from aiogram.types import Message, CallbackQuery
from ...keyboards.users.inline import zabrat_bonus_keyboard, poluchit, anketa_mentorstvo_keyboard
import Files
from messages import users as msg


async def SendLesson4(call: CallbackQuery):
    await call.answer()
    await call.message.answer_video(Files.lesson_4,
                                    caption=msg.lesson_4_caption)
    await call.message.answer('Основные ментальные триггеры успешных продаж',
                              reply_markup=zabrat_bonus_keyboard)
    await call.message.answer('Бонус  "слепые зоны" помогает, как личному бренду, так и бизнесу оценить и проработать слепые зоны',
                              reply_markup=poluchit)
    await call.message.answer(msg.last_message_,
                              reply_markup=anketa_mentorstvo_keyboard)

