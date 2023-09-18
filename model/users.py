"""
Таблица базы данных users, и модели доступа к ней
"""
import sqlalchemy
from pydantic import BaseModel, Field
from model.metadata import metadata

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String(32)),
    sqlalchemy.Column("last_name", sqlalchemy.String(32)),
    sqlalchemy.Column("email", sqlalchemy.String(48)),
    sqlalchemy.Column("password", sqlalchemy.String(32)),
    # Почему то эта конструкция не работает  - default - не работает
    # sqlalchemy.Column("created_at", sqlalchemy.DateTime(), default=datetime.utcnow), #
    sqlalchemy.Column("created_at", sqlalchemy.String(30)),
)


class UserIn(BaseModel):
    """
    Класс для хранения элемента данных с функциями проверки полей данных для записи и изменения данных
    """
    first_name: str = Field(title='first_name', description='User\'s first name', max_length=32)
    last_name: str = Field(title='last_name', description='User\'s last name', max_length=32)
    email: str = Field(title='email', description='User\'s email', max_length=48)
    password: str = Field(title='password', description='User\'s password', max_length=32)
#    created_at: datetime = Field(title='created_at', description='Date & time of creation', default=datetime.utcnow)

    def get_user(self):
        return {'first_name': self.first_name,
                'last_name': self.last_name,
                'email': self.email,
                'password': self.password,
                }


class User(BaseModel):
    """
    Класс для хранения элемента данных с функциями проверки полей данных для возвращения данных

    """
    id: int
    first_name: str = Field(title='first_name', description='User\'s first name', max_length=32)
    last_name: str = Field(title='last_name', description='User\'s last name', max_length=32)
    email: str = Field(title='email', description='User\'s email', max_length=48)
    password: str = Field(title='password', description='User\'s password', max_length=32)
#    created_at: datetime = Field(title='created_at', description='Date & time of creation', default=datetime.utcnow)

    def get_user(self):
        return {'id': self.id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'email': self.email,
                'password': self.password,
                'created_at': self.created_at,
                }
