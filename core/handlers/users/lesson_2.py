from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from ...keyboards.users.inline import zabrat_keyboard
import Files
from database import Connection
from messages import users as msg


async def SecondLesson2(call: CallbackQuery,
                        db: Connection):
    await call.answer()
    await db.updateLevel(call.from_user.id)
    await call.message.answer("Забирай шаблон смысловой карты, которая помогает структурировать построение контент-плана🎁")
    await call.message.answer_document(Files.mean_map)
    next_lessons = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text='Дальше ➡️',
            callback_data='sendLessonSecond'
        )
    ]])
    await call.message.answer("Продолжить смотреть уроки🏃🏼",
                              reply_markup=next_lessons)


async def SecondLesson2Next(call: CallbackQuery):
    await call.answer()
    await call.message.answer_video(Files.lesson_2,
                                    caption=msg.lesson_2_caption)
    await call.message.answer(msg.get_bonus_lesson_2,
                              reply_markup=zabrat_keyboard)
    
