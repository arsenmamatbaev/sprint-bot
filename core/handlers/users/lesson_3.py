from aiogram.types import Message, CallbackQuery
from ...keyboards.users.inline import zabrat_keyboard, toFourthLesson
import Files
from messages import users as msg


async def SendLesson3(call: CallbackQuery):
    await call.answer()
    await call.message.answer_video(Files.lesson_3,
                                    caption=msg.lesson_3_caption)
    await call.message.answer("Бонус🎁\nШаблон анкеты на предзапись")
    await call.message.answer_photo(Files.predzapis_example)
    await call.message.answer('Перехожу к 4 уроку🏃🏃‍♀',
                              reply_markup=toFourthLesson)

