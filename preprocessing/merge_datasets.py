import pandas as pd
new_data_types = {
    "ISBN" : "str",
    "TITLE" : "str",
    "AUTHOR" : "str",
    "PUBLICATION_YEAR" : "str",
    "PUBLISHER" : "str",
    "IMAGE_URL_S" : "str",
    "IMAGE_URL_M" : "str",
    "IMAGE_URL_L" : "str"
}
books = pd.read_csv("L1\\books_cleaned.csv", sep=";", on_bad_lines="warn", dtype=new_data_types, quotechar='"', escapechar="\\", encoding="utf-8")
books = books.drop(["IMAGE_URL_S", "IMAGE_URL_M", "IMAGE_URL_L"], axis="columns")
ratings_new_data_types = {
    "USER_ID": "str",
    "ISBN": "str",
    "RATING": "str",
}
ratings = pd.read_csv("L1\\book_ratings_cleaned.csv", sep=";", on_bad_lines="warn", dtype=ratings_new_data_types, quotechar='"', encoding="utf-8")

# inner join drops entries from books dataset which is not ideal - if these were tables in a DB we would obviously want to keep all the books
merged = pd.merge(books, ratings, how="inner")
print(merged.describe())
merged.to_csv("L1\\merged.csv", sep=";", encoding="utf-8")