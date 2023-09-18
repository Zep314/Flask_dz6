"""
Таблица базы данных orders, и модели доступа к ней
"""
import sqlalchemy
from pydantic import BaseModel, Field
from model.metadata import metadata
from sqlalchemy.orm import relationship


orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id")),
#    sqlalchemy.Column("user", relationship("Users", back_populates="orders")),
    sqlalchemy.Column("product_id", sqlalchemy.ForeignKey("products.id")),
#    sqlalchemy.Column("product", relationship("Products", back_populates="orders")),
    sqlalchemy.Column("order_date", sqlalchemy.String(30)),
    sqlalchemy.Column("order_status", sqlalchemy.String(32)),
    # Почему то эта конструкция не работает  - default - не работает
    # sqlalchemy.Column("created_at", sqlalchemy.DateTime(), default=datetime.utcnow), #
    sqlalchemy.Column("created_at", sqlalchemy.String(30)),
)


class OrderIn(BaseModel):
    """
    Класс для хранения элемента данных с функциями проверки полей данных для записи и изменения данных
    """
    user_id: int = Field(title='user_id', description='Order\'s user_id', gt=0)
    product_id: int = Field(title='product_id', description='Order\'s product_id', gt=0)
    order_date: str = Field(title='order_date', description='Order\'s date', max_length=30)
    order_status: str = Field(title='order_status', description='Order\'s status', max_length=32)
#    created_at: datetime = Field(title='created_at', description='Date & time of creation', default=datetime.utcnow)

    def get_order(self):
        return {'user_id': self.user_id,
                'product_id': self.product_id,
                'order_date': self.order_date,
                'order_status': self.order_status,
                }


class Order(BaseModel):
    """
    Класс для хранения элемента данных с функциями проверки полей данных для возвращения данных

    """
    id: int
    user_id: int = Field(title='user_id', description='Order\'s user_id', gt=0)
    product_id: int = Field(title='product_id', description='Order\'s product_id', gt=0)
    order_date: str = Field(title='order_date', description='Order\'s date', max_length=30)
    order_status: str = Field(title='order_status', description='Order\'s status', max_length=32)
#    created_at: datetime = Field(title='created_at', description='Date & time of creation', default=datetime.utcnow)

    def get_order(self):
        return {'id': self.id,
                'user_id': self.user_id,
                'product_id': self.product_id,
                'order_date': self.order_date,
                'order_status': self.order_status,
                'created_at': self.created_at,
                }
