from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonRequestUser


chooseUser = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text='Выбрать пользователя',
                request_user=KeyboardButtonRequestUser(request_id=5080)
            )
        ],
        [
            KeyboardButton(
                text='Отмена'
            )
        ]
    ], 
    resize_keyboard=True
)

