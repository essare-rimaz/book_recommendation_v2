import psycopg
from sqlalchemy import create_engine, String, Integer, MetaData
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
import pandas as pd


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "test_2"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))


class Book(Base):
    __tablename__ = "book"
    #ID: Mapped[int] = mapped_column(Integer, autoincrement=True)
    ISBN: Mapped[str] = mapped_column(primary_key=True)
    TITLE: Mapped[str] = mapped_column(String(30))
    TITLE_LOWERCASE: Mapped[str] = mapped_column(String(30))
    PUBLICATION_YEAR: Mapped[int] = mapped_column(Integer)
    PUBLISHER: Mapped[str] = mapped_column(String(30))

engine = create_engine("postgresql+psycopg://postgres:KpcOYPoXCog8AQ@localhost:5432/postgres")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()