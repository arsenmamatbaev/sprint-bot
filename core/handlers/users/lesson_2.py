from aiogram.types import Message, CallbackQuery
from ...keyboards.users.inline import zabrat_keyboard
import Files
from messages import users as msg


async def SecondLesson2(call: CallbackQuery):
    await call.answer()
    await call.message.answer_document(Files.mean_map)
    await call.message.answer("Забирай шаблон смысловой карты, которая помогает структурировать построение контент-плана🎁")
    await call.message.answer_video(Files.lesson_2,
                                    caption=msg.lesson_2_caption)
    await call.message.answer(msg.get_bonus_lesson_2,
                              reply_markup=zabrat_keyboard)

