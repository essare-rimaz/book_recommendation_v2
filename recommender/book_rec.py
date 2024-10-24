import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from database.models import Rating, Book
import recommender.schemas as schemas
from fastapi import status, Response


def get_book_details(input_book: str, db: Session):
    book_details = db.query(Book).filter(Book.ISBN == input_book).first()
    if not book_details:
        return Response(content="[]", status_code=status.HTTP_200_OK)
    return book_details


def get_book_ratings(input_book: str, db: Session):
    book_ratings = db.query(Rating).filter(Rating.ISBN == input_book).all()
    if not book_ratings:
        return Response(content="[]", status_code=status.HTTP_200_OK)

    return book_ratings

def get_user_ratings(user: int, db: Session):
    ratings = db.query(Rating).filter(Rating.USER_ID == user).all()
    if not ratings:
        return Response(content="[]", status_code=status.HTTP_200_OK)

    return ratings


def get_readers_of_input_book(input_book: str, db: Session):
    readers_statement = db.query(Rating.USER_ID).distinct().filter(Rating.ISBN == input_book)
    readers_subquery = readers_statement.subquery()
    readers_result = readers_statement.all()
    if not readers_result:
        return Response(content="[]", status_code=status.HTTP_200_OK)
    
    return readers_result, readers_subquery


def get_ratings_of_related_books(input_book: str, db: Session, threshold: int=8) -> pd.DataFrame:
    readers, readers_subquery = get_readers_of_input_book(input_book, db)
    #TODO i might have readers but they might not have rated any other books
    ranked_books = db.query(Rating.ISBN).filter(Rating.USER_ID.in_(select(readers_subquery))).group_by(Rating.ISBN).having(func.count(Rating.RATING)>threshold).subquery()
    ratings_per_user_and_book = db.query(Rating.USER_ID, Rating.ISBN, Rating.RATING).filter(Rating.ISBN.in_(select(ranked_books)))
    result = ratings_per_user_and_book
    df = pd.read_sql(result.statement, db.bind)
    df = df.pivot(index='USER_ID', columns='ISBN', values='RATING')

    return df

def get_books_correlation(correlation_dataset: pd.DataFrame, input_book: str) -> pd.Series:
    correlation_dataset.corr()
    input_book_correlations = correlation_dataset.corr()[input_book]
    input_book_correlations = input_book_correlations.rename("correlation")

    return input_book_correlations

def get_books_average_rating(correlation_dataset: pd.DataFrame) -> pd.Series:
    input_book_averages = correlation_dataset.mean()
    input_book_averages = input_book_averages.rename("average")

    return input_book_averages

def get_final_dataset(input_book_correlations: pd.Series, input_book_averages: pd.Series, input_book: str, db: Session, n: int=10, threshold: float=0.6) -> pd.DataFrame:
    values = pd.concat([input_book_averages, input_book_correlations], axis=1).reset_index()
    values = values[values["ISBN"] != input_book]
    values = values[values["correlation"] > threshold]
    values = values.sort_values('correlation', ascending = False).head(n)
    #TODO - does it have to be tuples?
    recommended_books = db.query(Book).filter(Book.ISBN.in_(tuple(values["ISBN"]))).all()
    values = values.reset_index(drop=True)

    response_list = [
        schemas.RecommendationOut(
            ISBN=row.ISBN,
            TITLE=row.TITLE,
            PUBLICATION_YEAR=row.PUBLICATION_YEAR,
            PUBLISHER=row.PUBLISHER,
            AVERAGE=values.query("ISBN == @row.ISBN")["average"].values,
            CORRELATION=values.query("ISBN == @row.ISBN")["correlation"].values
        )
        for row in recommended_books
    ]

    return response_list