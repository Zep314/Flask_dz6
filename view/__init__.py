"""
Init-файл для пакета с моими классами, переменными и функциями
"""

from view.user import create_user, update_user, delete_user, read_users
from view.product import create_product, update_product, delete_product, read_products
from view.order import create_order, update_order, delete_order, read_orders

# Эти классы, переменные и функции будем "экспортировать" для внешней работы
__all__ = ['create_user', 'update_user', 'delete_user', 'read_users',
           'create_product', 'update_product', 'delete_product', 'read_products',
           'create_order', 'update_order', 'delete_order', 'read_orders',
           ]
