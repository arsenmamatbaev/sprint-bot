import os
import asyncio
import logging
from dotenv.main import load_dotenv
#--------- aiogram ---------#
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
#--------- Database ---------#
import database
#------- Middlewares --------#
from core.middlewares.dbmiddleware import DbMiddleware
from core.middlewares.apschmiddleware import SchedulerMiddleware
from core.middlewares.prdmiddleware import ProdamusMiddleware
#--------- Handlers ---------#
from core.handlers.users.bot_start import start
#--------- Others ---------#
from prodamus import Prodamus
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler_di import ContextSchedulerDecorator

load_dotenv()

main_event_loop = asyncio.new_event_loop()
scheduler_event_loop = asyncio.new_event_loop()

db_config = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

prodamus = Prodamus()
bot = Bot(os.getenv('API_KEY'),
          parse_mode='html')
dp = Dispatcher()

scheduler = ContextSchedulerDecorator(AsyncIOScheduler(event_loop=scheduler_event_loop))

async def on_startup():
    logging.basicConfig(level=logging.INFO)
    scheduler.start()
    connection = await database.connect(**db_config)
    await connection.create_tables()
    dp.update.middleware.register(DbMiddleware(connection=connection))  # Мидлварь базы данных

async def main():
    #------- Middlewares --------#
    dp.update.middleware.register(SchedulerMiddleware(scheduler=scheduler))
    dp.update.middleware.register(ProdamusMiddleware(prodamus=prodamus))
    #--------- Handlers ---------#
    dp.message.register(start, CommandStart())

    #--------- Others ---------#
    dp.startup.register(on_startup)

    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == '__main__':
    main_event_loop.run_until_complete(main())
