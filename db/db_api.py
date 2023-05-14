import os
import time

from sqlalchemy import Engine, create_engine, exists, select, update, delete, or_
from sqlalchemy.orm import Session, joinedload
from sqlalchemy_utils import database_exists, create_database

from db.models import Base, User, Transfer


class Database:
    def __init__(self):
        self.engine = self.get_db_engine()

    def is_user_exists(self, login: str = None, card_number: str = None) -> bool:
        with Session(self.engine) as session:
            if login:
                return session.scalar(exists(User).where(User.login == login).select())
            return session.scalar(exists(User).where(User.card_number == card_number).select())

    def save_user(self, user_data: list[str]) -> None:
        with Session(self.engine) as session:
            session.add(
                User(card_number=int(user_data[0]), name=user_data[1], login=user_data[2], password=user_data[3]))
            session.commit()

    def login_user(self, login: str, password: str) -> User | None:
        with Session(self.engine) as session:
            return session.scalar(select(User)
                                  .where(User.login == login)
                                  .where(User.password == password))

    def is_login_data_correct(self, login: str, password: str):
        with Session(self.engine) as session:
            return session.scalar(exists(User).where(User.login == login).where(User.password == password).select())

    def change_balance(self, from_user: User, to_card: str, balance_changing: int) -> None:
        with Session(self.engine) as session:
            from_user.balance -= balance_changing
            session.add(from_user)
            to_user = session.scalar(select(User)
                                     .where(User.card_number == to_card))
            to_user.balance += balance_changing
            session.add(to_user)
            session.add(Transfer(from_user=from_user, to_user=to_user, amount=balance_changing, time=time.time()))
            session.commit()
            session.refresh(from_user)
            session.refresh(to_user)

    def get_all_operations(self, user: User, limit: int):
        with Session(self.engine) as session:
            raw_operations = session.scalars(select(Transfer).order_by(Transfer.time.desc())
                                             .where(or_(Transfer.from_user == user, Transfer.to_user == user))
                                             .options(joinedload(Transfer.from_user))
                                             .options(joinedload(Transfer.to_user)))
            operations = []
            for num, operation in enumerate(raw_operations):
                if num == limit:
                    break
                operations.append(operation)
                session.refresh(operation.to_user)
                session.refresh(operation.from_user)
            return operations

    @staticmethod
    def get_db_engine() -> Engine:
        engine = create_engine(os.getenv('DATABASE_URL'), echo=True)
        if not database_exists(engine.url):
            create_database(engine.url)

        Base.metadata.create_all(engine)
        return engine
