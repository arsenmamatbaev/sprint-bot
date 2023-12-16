from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


admin_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='⚙️Управление оплатой',
                callback_data='payment_settings'
            )
        ],
        [
            InlineKeyboardButton(
                text='💻Управление админами',
                callback_data='admin_settings'
            )
        ],
        [
            InlineKeyboardButton(
                text='🗂Управление пользователями',
                callback_data='user_settings'
            )
        ],
        [
            InlineKeyboardButton(
                text='📬Рассылки',
                callback_data='mailing'
            )
        ],
        [
            InlineKeyboardButton(
                text='💎Провести акцию',
                callback_data='diskount'
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


admins_settings_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='➕Добавить админа',
                callback_data='admin_add'
            )
        ],
        [
            InlineKeyboardButton(
                text='🗑Удалить админа',
                callback_data='admin_delete'
            )
        ],
        [
            InlineKeyboardButton(
                text='🔙В меню',
                callback_data='toMenu'
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

