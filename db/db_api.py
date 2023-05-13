import os

from sqlalchemy import Engine, create_engine, exists, select, update, delete
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

from db.models import Base, User


class Database:
    def __init__(self):
        self.engine = self.get_db_engine()

    def is_user_exists(self, name: str, card_number: int, login: str) -> None:
        with Session(self.engine) as session:
            return session.scalar(exists(User)
                                  .where(User.card_number == card_number, User.name == name, User.login == login)
                                  .select())

    def save_user(self, user_data: list[str]) -> None:
        with Session(self.engine) as session:
            session.add(
                User(card_number=int(user_data[0]), name=user_data[1], login=user_data[2], password=user_data[3]))
            session.commit()

    def login_user(self, password: str, card_number: int) -> None:
        with Session(self.engine) as session:
            return session.scalar(exists(User)
                                  .where(User.password == password, User.card_number == card_number)
                                  .select())

    @staticmethod
    def get_db_engine() -> Engine:
        engine = create_engine(os.getenv('DATABASE_URL'), echo=True)
        if not database_exists(engine.url):
            create_database(engine.url)

        Base.metadata.create_all(engine)
        return engine
