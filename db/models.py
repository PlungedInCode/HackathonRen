from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, ForeignKey

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    card_number: Mapped[str] = mapped_column(String(16), unique=True)
    name: Mapped[str] = mapped_column(String(200))
    login: Mapped[str] = mapped_column(String(200), unique=True)
    password: Mapped[str] = mapped_column(String(200))
    balance: Mapped[int] = mapped_column(Integer(), default=1000)


class Transfer(Base):
    __tablename__ = "transfers"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    from_user_id: Mapped[int] = mapped_column(Integer(), ForeignKey("users.id"))
    from_user: Mapped["User"] = relationship("User", foreign_keys=[from_user_id])
    to_user_id: Mapped[int] = mapped_column(Integer(), ForeignKey("users.id"))
    to_user: Mapped["User"] = relationship("User", foreign_keys=[to_user_id])
    time: Mapped[int] = mapped_column(Integer())
    amount: Mapped[int] = mapped_column(Integer())

