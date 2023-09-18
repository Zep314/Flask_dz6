"""
Модуль для представления дынных таблицы users
"""

import model as md
from datetime import datetime


async def create_user(user: md.UserIn):
    """
    Вставка новых данных
    :param user:
    :return:
    """
    query = md.users.insert().values(first_name=user.first_name,
                                     last_name=user.last_name,
                                     email=user.email,
                                     password=user.password,
                                     created_at=datetime.now().strftime("%d-%m-%Y, %H:%M:%S.%f"),
                                     )
    await md.database.execute(query)
    md.logger.info('Отработал POST запрос для таблицы users (вставка данных).')
    return user


async def update_user(user_id: int, new_user: md.UserIn):
    """
    Обновление данных
    :param user_id:
    :param new_user:
    :return:
    """
    query = md.users.update().where(md.users.c.id ==
                                    user_id).values(**new_user.dict())
    await md.database.execute(query)
    md.logger.info('Отработал PUT запрос для таблицы users (изменение данных) для user_id = {user_id}.')
    return {**new_user.dict(), "id": user_id}


async def delete_user(user_id: int):
    """
    Удаление данных
    :param user_id:
    :return:
    """
    query = md.users.delete().where(md.users.c.id == user_id)
    await md.database.execute(query)
    md.logger.info(f'Отработал DELETE запрос для user_id = {user_id} по таблице users.')
    return {'message': 'User deleted'}


async def read_users():
    """
    Чтение данных
    :return:
    """
    query = md.users.select()
    md.logger.info(f'Отработал GET запрос (users). Вернул всю таблицу.')
    return await md.database.fetch_all(query)

