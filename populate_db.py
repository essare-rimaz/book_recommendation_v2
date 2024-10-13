import pandas as pd
from db import get_db

new_data_types = {
    "ISBN" : "str",
    "TITLE" : "str",
    "TITLE_LOWERCASE" : "str",
    "AUTHOR" : "str",
    "PUBLICATION_YEAR" : "int",
    "PUBLISHER" : "str",

}

books = pd.read_csv("L1\\books_cleaned.csv", sep=";", on_bad_lines="warn", dtype=new_data_types, quotechar='"', escapechar="\\", encoding="utf-8")
books.to_sql('book', get_db(), if_exists='replace', index=False)