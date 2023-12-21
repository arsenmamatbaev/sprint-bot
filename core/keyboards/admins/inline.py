from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


admin_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                    text='Изменить цены',
                    callback_data='edit_price'
            )
        ],
        [
            InlineKeyboardButton(
                text='📬Рассылка',
                callback_data='mailing'
            )
        ],      
        [
            InlineKeyboardButton(
                text='📋Список пользователей(Excel)',
                callback_data='user_list'
            )
        ]
    ]
)


cancel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Отменить',
                callback_data='cancel'
            )
        ]
    ]
)

