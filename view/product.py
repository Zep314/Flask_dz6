"""
Модуль для представления дынных таблицы products
"""

import model as md
from datetime import datetime


async def create_product(product: md.ProductIn):
    """
    Вставка новых данных
    :param product:
    :return:
    """
    query = md.products.insert().values(name=product.name,
                                        description=product.description,
                                        cost=product.cost,
                                        created_at=datetime.now().strftime("%d-%m-%Y, %H:%M:%S.%f"),
                                        )
    await md.database.execute(query)
    md.logger.info('Отработал POST запрос для таблицы products (вставка данных).')
    return product


async def update_product(product_id: int, new_product: md.ProductIn):
    """
    Обновление данных
    :param product_id:
    :param new_product:
    :return:
    """
    query = md.products.update().where(md.products.c.id ==
                                       product_id).values(**new_product.model_dump())
    await md.database.execute(query)
    md.logger.info('Отработал PUT запрос для таблицы products (изменение данных) для product_id = {product_id}.')
    return {**new_product.model_dump(), "id": product_id}


async def delete_product(product_id: int):
    """
    Удаление данных
    :param product_id:
    :return:
    """
    query = md.products.delete().where(md.products.c.id == product_id)
    await md.database.execute(query)
    md.logger.info(f'Отработал DELETE запрос для product_id = {product_id} по таблице products.')
    return {'message': 'Product deleted'}


async def read_products():
    """
    Чтение данных
    :return:
    """
    query = md.products.select()
    md.logger.info(f'Отработал GET запрос (products). Вернул всю таблицу.')
    return await md.database.fetch_all(query)
