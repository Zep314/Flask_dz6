"""
Модуль для представления дынных таблицы orders
"""

import model as md
from datetime import datetime


async def create_order(order: md.OrderIn):
    """
    Вставка новых данных
    :param order:
    :return:
    """
    query = md.orders.insert().values(user_id=order.user_id,
                                      product_id=order.product_id,
                                      order_date=order.order_date,
                                      order_status=order.order_status,
                                      created_at=datetime.now().strftime("%d-%m-%Y, %H:%M:%S.%f"),
                                      )
    await md.database.execute(query)
    md.logger.info('Отработал POST запрос для таблицы orders (вставка данных).')
    return order


async def update_order(order_id: int, new_order: md.OrderIn):
    """
    Обновление данных
    :param order_id:
    :param new_order:
    :return:
    """
    query = md.orders.update().where(md.orders.c.id ==
                                     order_id).values(**new_order.dict())
    await md.database.execute(query)
    md.logger.info('Отработал PUT запрос для таблицы orders (изменение данных) для order_id = {order_id}.')
    return {**new_order.dict(), "id": order_id}


async def delete_order(order_id: int):
    """
    Удаление данных
    :param order_id:
    :return:
    """
    query = md.orders.delete().where(md.orders.c.id == order_id)
    await md.database.execute(query)
    md.logger.info(f'Отработал DELETE запрос для order_id = {order_id} по таблице orders.')
    return {'message': 'Order deleted'}


async def read_orders():
    """
    Чтение данных
    :return:
    """
    query = md.orders.select()
    md.logger.info(f'Отработал GET запрос (orders). Вернул всю таблицу.')
    return await md.database.fetch_all(query)
