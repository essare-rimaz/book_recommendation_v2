from fastapi import FastAPI, Depends
from db import get_db, Book
from pydantic import BaseModel
from sqlalchemy.orm import Session
import schemas
from typing import List



app = FastAPI()


@app.get("/recommendations/{isbn}", response_model=schemas.RecommendationOut)
def get_recommendations(isbn: str, db: Session = Depends(get_db)):
    books = db.query(Book).filter(Book.ISBN == isbn).first()
    return books