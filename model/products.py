"""
Таблица базы данных products, и модели доступа к ней
"""
import sqlalchemy
from pydantic import BaseModel, Field
from model.metadata import metadata
from sqlalchemy.orm import relationship


products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(32)),
    sqlalchemy.Column("description", sqlalchemy.String(32)),
    sqlalchemy.Column("cost", sqlalchemy.Float),
    # Почему то эта конструкция не работает  - default - не работает
    # sqlalchemy.Column("created_at", sqlalchemy.DateTime(), default=datetime.utcnow), #
    sqlalchemy.Column("created_at", sqlalchemy.String(30)),
#    orders=relationship("Product", back_populates="users"),
)


class ProductIn(BaseModel):
    """
    Класс для хранения элемента данных с функциями проверки полей данных для записи и изменения данных
    """
    name: str = Field(title='name', description='Product\'s name', max_length=32)
    description: str = Field(title='description', description='Product\'s description', max_length=150)
    cost: float = Field(title='cost', description='Product\'s cost', ge=0)
#    created_at: datetime = Field(title='created_at', description='Date & time of creation', default=datetime.utcnow)

    def get_product(self):
        return {'name': self.name,
                'description': self.description,
                'cost': f'{self.cost:.2f}',
                }


class Product(BaseModel):
    """
    Класс для хранения элемента данных с функциями проверки полей данных для возвращения данных
    """
    id: int
    name: str = Field(title='name', description='Product\'s name', max_length=32)
    description: str = Field(title='description', description='Product\'s description', max_length=150)
    cost: float = Field(title='cost', description='Product\'s cost', ge=0)
#    created_at: datetime = Field(title='created_at', description='Date & time of creation', default=datetime.utcnow)
    created_at: str = Field(title='created_at', description='Date & time of creation', max_length=30)

    def get_product(self):
        return {'id': self.id,
                'name': self.name,
                'description': self.description,
                'cost': f'{self.cost:.2f}',
                'created_at': self.created_at,
                }
