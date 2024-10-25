from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint, Identity, Boolean, event, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pydantic import EmailStr
from .populate_db import populate_books, populate_ratings, populate_users

from .db import Base

class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "book"

    ISBN: Mapped[str] = mapped_column(String(30), primary_key=True, nullable=False)
    TITLE: Mapped[str] = mapped_column(nullable=False)
    AUTHOR: Mapped[str] = mapped_column(nullable=False)
    PUBLICATION_YEAR: Mapped[int] = mapped_column(Integer, nullable=False)
    PUBLISHER: Mapped[str] = mapped_column(nullable=False)

class Rating(Base):
    __tablename__ = "rating"
    ID: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True, nullable=False, autoincrement=True) #identity autogenerates sequence for PK when populating table
    USER_ID: Mapped[int] = mapped_column(ForeignKey("user.USER_ID"), nullable=False)
    ISBN: Mapped[str] = mapped_column(ForeignKey("book.ISBN"), nullable=False)
    RATING: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("USER_ID", "ISBN"),
    )

class User(Base):
    __tablename__ = "user"
    USER_ID: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True, nullable=False, autoincrement=True)
    EMAIL: Mapped[EmailStr] = mapped_column(String, nullable=False)
    PASSWORD_HASH: Mapped[str] = mapped_column(String, nullable=False)
    DISABLED_BOOLEAN: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="False")

    __table_args__ = (
        UniqueConstraint("EMAIL"),
    )

@event.listens_for(Book.__table__, 'after_create')
def populate_book_after_create(mapper, connection, **kw):
    print("table Book was just created")
    populate_books(connection)

@event.listens_for(Rating.__table__, 'after_create')
def populate_rating_after_create(mapper, connection, **kw):
    print("table Rating was just created")
    populate_ratings(connection)
    reset_sequence_query = text("""
    SELECT setval(pg_get_serial_sequence('user', 'USER_ID'), (SELECT MAX("USER_ID") FROM public.user));
    """)
    connection.execute(reset_sequence_query)

@event.listens_for(User.__table__, 'after_create')
def populate_user_after_create(mapper, connection, **kw):
    print("table User was just created")
    populate_users(connection)