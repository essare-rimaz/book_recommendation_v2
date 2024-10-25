from fastapi import FastAPI, Depends

from typing import List

from sqlalchemy.orm import Session
from database.db import engine, get_db

from database import models

import schemas as schemas
import book_rec as book_rec

from routers import users

models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(users.router)


@app.get("/recommendations/{isbn}", response_model=List[schemas.RecommendationOut], tags=["recommendations"])
def get_recommendations(
    isbn: str, 
    db: Session = Depends(get_db)
):
    corr_dataset = book_rec.get_ratings_of_related_books(isbn, db)
    correlations = book_rec.get_books_correlation(corr_dataset, isbn)
    averages = book_rec.get_books_average_rating(corr_dataset)
    recommendations = book_rec.get_final_dataset(correlations, averages, isbn, db)

    return recommendations


@app.get("/books/{isbn}", response_model=schemas.BookOut, tags=["books"])
def get_books(
    isbn: str, 
    db: Session = Depends(get_db)
):
    book_details = book_rec.get_book_details(isbn, db)

    return book_details


@app.get("/ratings/{isbn}", response_model=List[schemas.RatingOut], tags=["ratings"])
def get_ratings(
    isbn: str, 
    db: Session = Depends(get_db)
):
    ratings = book_rec.get_book_ratings(isbn, db)

    return ratings