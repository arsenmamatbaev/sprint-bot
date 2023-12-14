from flask import Flask, request, Response


app = Flask(__name__)


@app.route('/payment')
async def newPayment():
    data = request.values.to_dict()
    if data['payment_status'] == 'succes':
        try:
            user_id = int(data['order_id'])
            payment_sum = int(data['sum'])
            print(f'{user_id}\n{payment_sum}')
        except:
            return Response('Возникла какая-то ошибка в процессе обработки платежа',
                            status=405)
    else:
        return Response("Status is not 'succes'",
                        status=400)


class ProdamusListener:
    '''
    Класс слушателя платежной системы
    '''
    def __init__(self,
                 host: str = '127.0.0.1',
                 port: int = 5874) -> None:
        '''
        Создает объект класса слушателя
        '''
        self.__host = host
        self.__port = port

    
    def start_listen(self) -> None:
        '''
        Запуск прослушивания
        '''
        app.run(self.__host,
                self.__port)

