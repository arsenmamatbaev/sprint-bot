import asyncpg
import logging
from typing import Union
import pytz
from datetime import datetime, timedelta
from .UserObject import User, DataUser, PaymentData
from .levels import Levels

tz = pytz.timezone('Europe/Moscow')

class Connection:
    """
    Соединение с базой данных
    """
    def __init__(self,
                 connection: asyncpg.Connection) -> None:
        '''
        Создание соединения с БД
        '''
        self.__conn = connection

    async def create_tables(self) -> None:
        '''
        Создание всех необходимых таблиц
        '''
        table_users = ("CREATE TABLE IF NOT EXISTS users("
                       "id SERIAL PRIMARY KEY,"
                       "user_id BIGINT UNIQUE NOT NULL,"
                       "full_name VARCHAR(250) NOT NULL,"
                       "username VARCHAR(50),"
                       f"level VARCHAR(50) DEFAULT '{Levels.payment_1}',"
                       "payment_link VARCHAR(50),"
                       "payment_date VARCHAR(50) DEFAULT ' ',"
                       "updated_at VARCHAR(50) DEFAULT ' ',"
                       "register_date VARCHAR(50));")
        await self.__conn.execute(table_users)
        table_settings = ("CREATE TABLE IF NOT EXISTS settings("
                          "price1 INTEGER DEFAULT 1490,"
                          "price2 INTEGER DEFAULT 3770,"
                          "expire INTEGER DEFAULT 3);")
        await self.__conn.execute(table_settings)
        table_admins = ("CREATE TABLE IF NOT EXISTS admins("
                        "id SERIAL PRIMARY KEY,"
                        "user_id BIGINT UNIQUE NOT NULL,"
                        "full_name VARCHAR(250),"
                        "username VARCHAR(50));")
        await self.__conn.execute(table_admins)
        logging.info('Создание таблиц --> Succes')

    async def userExist(self,
                        user: User) -> Union[DataUser, bool]:
        '''
        Проверяет наличие пользователя в базе данных
        '''
        query = f"SELECT * FROM users WHERE user_id = {user.user_id}"
        ExistUser = await self.__conn.fetch(query)
        if not ExistUser:
            return False
        return DataUser(
            user_id=user.user_id,
            full_name=user.full_name,
            username=user.username,
            payment_link=ExistUser[0]['payment_link'],
            level=ExistUser['level']
        )
    
    async def create_or_update(self,
                               user: User,
                               payment_link) -> None:
        '''
        Создает/обновляет пользователя в базе данных
        '''
        now_date = datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M')
        query = ("INSERT INTO users (user_id, full_name, username, payment_link, register_date) "
                 f"VALUES ({user.user_id}, '{user.full_name}', '{user.username}', '{payment_link.payment_link}', '{now_date}') "
                 f"ON CONFLICT (user_id) DO UPDATE SET updated_at = '{now_date}', payment_link = '{payment_link.payment_link}'")
        await self.__conn.execute(query)

    @property
    async def getPaymentData(self) -> PaymentData:
        query = "SELECT * FROM settings;"
        data = await self.__conn.fetchrow(query)

        return PaymentData(
            price1=data['price1'],
            price2=data['price2'],
            expire=data['expire']
        )

