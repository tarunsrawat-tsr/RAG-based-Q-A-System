from sqlalchemy.engine import create_engine
from sqlalchemy.orm import DeclarativeBase
from pgvector.sqlalchemy import Vector
from sqlalchemy import ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from typing import TypedDict, List, Dict

class Chat(TypedDict):
    user_message: str
    response: str

class Base(DeclarativeBase):
    """ Base class """
    pass

class Users(Base):
    """ Defined user_accounts table for database"""

    __tablename__ = "user_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    email_address: Mapped[str] = mapped_column(String(30), nullable=False)
    password: Mapped[str] = mapped_column(String(30), nullable=False)

    email: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    sessions: Mapped[List["Sessions"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

class Address(Base):
    """ Stores email address for user_accounts """

    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_accounts.id"))
    email_address: Mapped[str] = mapped_column(String(255), nullable=False)
    user: Mapped["Users"] = relationship(back_populates="email")

    @validates("email_address")
    def validate_email(self, key, val):
        """ Validates email address ensures they end with requied domains only """
        if not val or not val.lower().endswith("@gmail.com"):
            raise ValueError("Invalid email address found!.")
        return val

class Sessions(Base):
    """ User Chats/Sessions """

    __tablename__ = "session"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_accounts.id"), nullable=False)
    messages: Mapped[List[Dict[str,any]]] = mapped_column(JSON, nullable=False)

    user: Mapped["Users"] = relationship(back_populates="sessions")


class VectorDB(Base):
    """ Vector Database for RAG system """

    __tablename__ = "vector_db"

    index: Mapped[int] = mapped_column(primary_key=True)
    chunk: Mapped[str] = mapped_column(String(500), nullable=False)
    embedding: Mapped[Vector] = mapped_column(Vector(1536), nullable=False)