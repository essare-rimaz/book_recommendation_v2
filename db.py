from typing import List
from sqlalchemy import create_engine, String, Integer, ForeignKey, UniqueConstraint, Identity, Boolean
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship
from pydantic import EmailStr

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


engine = create_engine("postgresql+psycopg://postgres:KpcOYPoXCog8AQ@localhost:5432/postgres")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()