import os

from sqlalchemy import Engine, create_engine
from sqlalchemy_utils import database_exists, create_database

from db.models import Base


class Database:
    def __init__(self):
        self.engine = self.get_db_engine()

    # Пишем тут методы, которые нужны для работы с базой

    @staticmethod
    def get_db_engine() -> Engine:
        engine = create_engine(os.getenv('DATABASE_URL'), echo=True)
        if not database_exists(engine.url):
            create_database(engine.url)

        Base.metadata.create_all(engine)
        return engine
