import pandas as pd
#from models import User, Book, Rating
from pathlib import Path

relative_path = Path("preprocessing/L1/books_cleaned.csv")

def populate_books(engine):
    new_data_types = {
        "ISBN" : "str",
        "TITLE" : "str",
        "AUTHOR" : "str",
        "PUBLICATION_YEAR" : "int",
        "PUBLISHER" : "str",

    }

    books = pd.read_csv(Path("database/preprocessing/L1/books_cleaned.csv").resolve(), sep=";", on_bad_lines="warn", dtype=new_data_types, quotechar='"', escapechar="\\", encoding="utf-8")
    books.to_sql('book', engine, if_exists='append', index=False)


def populate_users(engine):
    users_types = {
    #    "ID": "str",
        "USER_ID": "int",
        "EMAIL": "str",
        "PASSWORD": "str",
        "DISABLED_BOOLEAN": "bool"
    }
    users = pd.read_csv(Path("database/preprocessing/L1/users_cleaned.csv").resolve(), sep=";", on_bad_lines="warn", dtype=users_types, quotechar='"', encoding="utf-8")
    users.to_sql('user', engine, if_exists='append', index=False)


def populate_ratings(engine):
    ratings_new_data_types = {
        "USER_ID": "int",
        "ISBN": "str",
        "RATING": "int",
    }
    ratings = pd.read_csv(Path("database/preprocessing/L1/book_ratings_cleaned.csv").resolve(), sep=";", on_bad_lines="warn", dtype=ratings_new_data_types, quotechar='"', encoding="utf-8")
    ratings.to_sql('rating', engine, if_exists='append', index=False)