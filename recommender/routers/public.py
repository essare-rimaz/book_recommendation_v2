from fastapi import Depends, APIRouter

from typing import List

from sqlalchemy.orm import Session
from database.db import get_db

import schemas as schemas
import book_rec as book_rec

router = APIRouter(
    prefix="",
)


@router.get("/recommendations/{isbn}", response_model=List[schemas.RecommendationOut], tags=["recommendations"])
def get_recommendations(
    isbn: str, 
    db: Session = Depends(get_db),
    summary="Get a book recommendation based on what you like already"
):
    '''
    Based on ISBN of a book you like, get a list of book items that you might like as well.

    Try it with an example 0679429220
    '''
    corr_dataset = book_rec.get_ratings_of_related_books(isbn, db)
    correlations = book_rec.get_books_correlation(corr_dataset, isbn)
    averages = book_rec.get_books_average_rating(corr_dataset)
    recommendations = book_rec.get_final_dataset(correlations, averages, isbn, db)

    return recommendations


@router.get("/books/{isbn}", response_model=schemas.BookOut, tags=["books"])
def get_books(
    isbn: str, 
    db: Session = Depends(get_db),
    summary="Get detailed information about a book"
):
    book_details = book_rec.get_book_details(isbn, db)

    return book_details


@router.get("/ratings/{isbn}", response_model=List[schemas.RatingOut], tags=["ratings"])
def get_ratings(
    isbn: str, 
    db: Session = Depends(get_db),
    summary="Get ratings of a book - the higher the better"
):
    ratings = book_rec.get_book_ratings(isbn, db)

    return ratings