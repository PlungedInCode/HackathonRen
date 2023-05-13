from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

Base = declarative_base()

# Пишем тут модель
class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    card_number: Mapped[int] = mapped_column(Integer())
    name: Mapped[str] = mapped_column(String(200))
    login: Mapped[str] = mapped_column(String(200))
    password: Mapped[str] = mapped_column(String(200))
    # nofications


# class Account(Base):
#     __tablename__ = "Account"
#     user_id: Mapped[int] = mapped_column(Integer())
#     balance: Mapped[float] = mapped_column(Float())