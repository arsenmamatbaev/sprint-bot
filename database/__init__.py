import logging
import asyncpg
from .connection import Connection
from .UserObject import User


async def connect(host: str = '127.0.0.1',
                  port: int = 5432,
                  user: str = 'postgres',
                  password: str = 'postgres') -> Connection:
    '''
    Подключение к базе данных
    :return: Соединение с БД 
    '''
    connection = await asyncpg.connect(host=host,
                                       port=port,
                                       user=user,
                                       password=password)
    logging.info('Подключение к базе данных --> Succes')

    return Connection(
        connection=connection
    )

