from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#engine = create_engine("postgresql+psycopg://postgres:KpcOYPoXCog8AQ@localhost:5432/postgres")
engine = create_engine("postgresql+psycopg://postgres:password123@postgres:5432/postgres")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()