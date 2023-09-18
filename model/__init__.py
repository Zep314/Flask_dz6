"""
Init-файл для пакета с моими классами, переменными и функциями
"""
from model.metadata import metadata, database, DATABASE_URL
from model.my_logger import logger
from model.users import users, User, UserIn
from model.products import products, Product, ProductIn
from model.orders import orders, Order, OrderIn


# Эти классы, переменные и функции будем "экспортировать" для внешней работы
__all__ = ['metadata', 'database', 'logger', 'DATABASE_URL',
           'users', 'User', 'UserIn',
           'products', 'Product', 'ProductIn',
           'orders', 'Order', 'OrderIn',
           ]
