import pytz
import requests
import time
from datetime import datetime, timedelta
from database import User, Connection
from .ProdamusObject import PaymentLink

tz = pytz.timezone('Europe/Moscow')

class Prodamus:
    """
    Класс платежной системы Prodamus
    """
    def __init__(self,
                 mainUrl: str = 'https://oxanaamel.payform.ru/') -> None:
        '''
        Создание объекта класса Prodamus
        '''
        self.__newLink = mainUrl + '?order_id={order_id}&products[0][price]={price}&products[0][quantity]=1&products[0][name]=Обучающие материалы&customer_extra=Полная оплата курса&do=link'
        self.__newLinkExpire = self.__newLink + '&link_expired={expire_date}'

    async def createLink(self,
                         user: User,
                         db: Connection,
                         level: int = 1) -> PaymentLink:
        '''
        Создание платежной ссылки от Prodamus
        :param level: Уровень ссылки: 1 -> Новая ссылка; 2 -> Обновленная ссылка;
        '''
        payment_data = await db.getPaymentData
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"}
        now_date = datetime.now(tz=tz)
        if level == 1:
            expire_date = now_date + timedelta(hours=payment_data.expire)
            mainLink = self.__newLinkExpire.format(order_id=user.user_id, 
                                                   price=payment_data.price1,
                                                   expire_date=expire_date.strftime('%Y-%m-%d %H:%M'))
            link = requests.get(mainLink, headers=headers).text
        else:
            mainLink = self.__newLink.format(order_id=user.user_id,
                                             price=payment_data.price2)
            link = requests.get(mainLink, headers=headers).text
        return PaymentLink(
            user=user,
            payment_link=link
        )

