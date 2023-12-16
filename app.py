import os
import asyncio
import logging
from dotenv.main import load_dotenv
#--------- aiogram ---------#
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command, StateFilter
#--------- Database ---------#
import database
from database import Connection
#------- Middlewares --------#
from core.middlewares.dbmiddleware import DbMiddleware
from core.middlewares.apschmiddleware import SchedulerMiddleware
from core.middlewares.prdmiddleware import ProdamusMiddleware
#--------- Filters ---------#
from aiogram import F
from core.filters.IsAdmin import IsAdmin
#--------- Handlers ---------#
from core.handlers.users.bot_start import start
from core.handlers.users.lesson_2 import SecondLesson2
from core.handlers.users.lesson_3 import SendLesson3
from core.handlers.users.lesson_4 import SendLesson4

from payment import SendFirstLesson


from core.handlers.admins.admin_start import start_admin
from core.handlers.admins.adminMenu import main_menu_handler, add_admin, choose_user_handler, toManiMenuHandler
#--------- Others ---------#
from States import AdminsStates, UsersStates
from prodamus import Prodamus
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler_di import ContextSchedulerDecorator

load_dotenv()

main_event_loop = asyncio.new_event_loop()

db_config = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

prodamus = Prodamus()
bot = Bot(os.getenv('API_KEY'),
          parse_mode='html',
          protect_content=True)
dp = Dispatcher()

scheduler = ContextSchedulerDecorator(AsyncIOScheduler())
scheduler.ctx.add_instance(instance=bot, 
                           declared_class=Bot)
scheduler.ctx.add_instance(instance=prodamus,
                           declared_class=Prodamus)

async def on_startup():
    logging.basicConfig(level=logging.INFO)
    connection = await database.connect(**db_config)
    await connection.create_tables()
    dp.update.middleware.register(DbMiddleware(connection=connection))  # Мидлварь базы данных
    scheduler.ctx.add_instance(instance=connection,
                               declared_class=Connection)
    scheduler.start()

async def main():
    dp.message.register(SendFirstLesson, Command('get_lessons'))
    #------- Middlewares --------#
    dp.update.middleware.register(SchedulerMiddleware(scheduler=scheduler))
    dp.update.middleware.register(ProdamusMiddleware(prodamus=prodamus))
    #--------- Handlers ---------#
    dp.message.register(start, CommandStart())
    dp.callback_query.register(SecondLesson2, F.data == 'get_request')
    dp.callback_query.register(SendLesson3, F.data == 'zabrat')
    dp.callback_query.register(SendLesson4, F.data == 'toFourthLesson')

    #--------- Admin's Handlers ---------#
    dp.callback_query.register(toManiMenuHandler, F.data == 'toMenu')
    dp.message.register(start_admin, Command(commands=['admin']), IsAdmin())
    dp.callback_query.register(main_menu_handler, StateFilter(AdminsStates.main_menu))
    dp.callback_query.register(add_admin, StateFilter(AdminsStates.admin_settings_menu))
    dp.message.register(choose_user_handler, StateFilter(AdminsStates.choose_user_menu))
    #--------- Others ---------#
    dp.startup.register(on_startup)

    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == '__main__':
    main_event_loop.run_until_complete(main())
