"""
Модуль для общих объектов базы данных
"""
import sqlalchemy
import databases

metadata = sqlalchemy.MetaData()

DB_FILENAME = 'my_database.db'  # Путь к файлу базы данных
DATABASE_URL = f"sqlite:///{DB_FILENAME}"
database = databases.Database(DATABASE_URL)  # , connect_args={"check_same_thread": False}
