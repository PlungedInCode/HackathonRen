from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

Base = declarative_base()


# Пишем тут модель
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    card_number: Mapped[int] = mapped_column(Integer(), unique=True)
    name: Mapped[str] = mapped_column(String(200))
    login: Mapped[str] = mapped_column(String(200), unique=True)
    password: Mapped[str] = mapped_column(String(200))
    balance: Mapped[int] = mapped_column(Integer(), default=1000)
