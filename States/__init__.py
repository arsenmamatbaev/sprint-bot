from aiogram.fsm.state import StatesGroup, State


class UsersStates(StatesGroup):
    ...


class AdminsStates(StatesGroup):
    main_menu = State()
    admin_settings_menu = State()
    choose_user_menu = State()

