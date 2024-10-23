import pandas as pd
from db import engine, User, get_db, sessionmaker
import string
import secrets


new_data_types = {
    "ISBN" : "str",
    "TITLE" : "str",
    "AUTHOR" : "str",
    "PUBLICATION_YEAR" : "int",
    "PUBLISHER" : "str",

}

books = pd.read_csv("L1\\books_cleaned.csv", sep=";", on_bad_lines="warn", dtype=new_data_types, quotechar='"', escapechar="\\", encoding="utf-8")
books.to_sql('book', engine, if_exists='append', index=False)
existing_books = books["ISBN"]

ratings_new_data_types = {
    "USER_ID": "int",
    "ISBN": "str",
    "RATING": "int",
}
ratings = pd.read_csv("L1\\book_ratings_cleaned.csv", sep=";", on_bad_lines="warn", dtype=ratings_new_data_types, quotechar='"', encoding="utf-8")
ratings = ratings.query('ISBN in @existing_books')



users_types = {
#    "ID": "str",
    "USER_ID": "int",
    "EMAIL": "str",
    "PASSWORD": "str",
    "DISABLED_BOOLEAN": "bool"
}
users = pd.read_csv("L1\\users_cleaned.csv", sep=";", on_bad_lines="warn", dtype=users_types, quotechar='"', encoding="utf-8")
users.to_sql('user', engine, if_exists='append', index=False)
#'SELECT setval(pg_get_serial_sequence('user', 'USER_ID'), (SELECT MAX("USER_ID") FROM public.user));'



ratings.to_sql('rating', engine, if_exists='append', index=False)
