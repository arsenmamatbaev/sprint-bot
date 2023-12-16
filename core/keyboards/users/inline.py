from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import Files


get_guide = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Забрать гайд',
                                                                        url='https://www.notion.so/6c5d093cc4394635af7148ef21c2428d?pvs=4')]])


anketa_mentorstvo_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Заполнить анкету',
            url=Files.anketa_mentorstvo
        )
    ]
])


get_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Получить',
            callback_data='get_request'
        )
    ]
])


zabrat_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Забрать 🎁',
            callback_data='zabrat'
        )
    ]
])

zabrat_bonus_keyboard = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(
        text='Забрать бонус🎁',
        url='https://dour-soil-e7a.notion.site/6c5d093cc4394635af7148ef21c2428d'
    )
]])

toFourthLesson = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(
        text='Смотреть 4 урок',
        callback_data='toFourthLesson'
    )
]])

poluchit = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(
        text="Забрать бонусный файл",
        url="https://disk.yandex.ru/i/2HNywHF9WoMNyQ"
    )
]])
