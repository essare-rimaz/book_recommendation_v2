import pandas as pd
from sqlalchemy import event, text
from database.models import User, Book, Rating

def populate_books(engine):
    new_data_types = {
        "ISBN" : "str",
        "TITLE" : "str",
        "AUTHOR" : "str",
        "PUBLICATION_YEAR" : "int",
        "PUBLISHER" : "str",

    }

    books = pd.read_csv("L1\\books_cleaned.csv", sep=";", on_bad_lines="warn", dtype=new_data_types, quotechar='"', escapechar="\\", encoding="utf-8")
    books.to_sql('book', engine, if_exists='append', index=False)


def populate_users(engine):
    users_types = {
    #    "ID": "str",
        "USER_ID": "int",
        "EMAIL": "str",
        "PASSWORD": "str",
        "DISABLED_BOOLEAN": "bool"
    }
    users = pd.read_csv("L1\\users_cleaned.csv", sep=";", on_bad_lines="warn", dtype=users_types, quotechar='"', encoding="utf-8")
    users.to_sql('user', engine, if_exists='append', index=False)


def populate_ratings(engine):
    ratings_new_data_types = {
        "USER_ID": "int",
        "ISBN": "str",
        "RATING": "int",
    }
    ratings = pd.read_csv("L1\\book_ratings_cleaned.csv", sep=";", on_bad_lines="warn", dtype=ratings_new_data_types, quotechar='"', encoding="utf-8")
    ratings.to_sql('rating', engine, if_exists='append', index=False)

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