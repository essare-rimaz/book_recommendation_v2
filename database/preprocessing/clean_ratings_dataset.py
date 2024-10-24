import pandas as pd

data_types = {
    "User-ID": "str",
    "ISBN": "str",
    "Book-Rating": "Int64"
}

ratings_new_col_names = {
    "User-ID": "USER_ID",
    "ISBN": "ISBN",
    "Book-Rating": "RATING",
}

ratings_new_data_types = {
    "USER_ID": "str",
    "ISBN": "str",
    "RATING": "str",
}

replacements = {
    b"&amp;": b"\x26", # ampersant with an ; confuses csv
    b"&#160;": b" ", # replace unbreakable space html entity with a space (dependent on &amp; replacement)
    b"&lt;br>": b"", # html entity (dependent on &amp; replacement)
    b"&lt;i>": b"", # html entity (dependent on &amp; replacement)
    b"&lt;/i>": b"", # html entity (dependent on &amp; replacement)
    b"&reg;": b"\xc2\xae", # html entity (dependent on &amp; replacement)
    b"\xc3?\xc2": b"\xc3", # lower case umlauts
    b"\r\n": b"\n", # legacy windows \r
    b'\\"': b"\\'", # escaped quotes

}

forbidden_squences = [b"\xc3?\xc2?", b"\xc2?", b"\xc3?", 
                      b"\xba", b"\xdf", b"\xc9", b"\xa1", b"\xa7", b"\xb4", b"0xdc", b"0xdc"] # specifically for ratings

with open("L1\\book_ratings_intermediary.csv", "w", encoding="utf-8") as out_file:
    pass

with open("L0\\BX-Book-Ratings.csv", "rb") as file:
    lines = file.readlines()

with open("L1\\book_ratings_intermediary.csv", "a", encoding="utf-8") as out_file:
    for line in lines:
        for sequence, replacement_sequence in replacements.items(): 
            sequence_occurences = line.count(sequence)
            if sequence_occurences > 0:
                line = line.replace(sequence, replacement_sequence)
        if any(forbiden_sequence in line for forbiden_sequence in forbidden_squences):
            continue
        try:
            decoded_line = line.decode("utf-8")
            out_file.write(decoded_line)
        except UnicodeDecodeError:
            print(f"Skipping line due to decoding error: {line}")
            continue

ratings = pd.read_csv("L1\\book_ratings_intermediary.csv", sep=";", on_bad_lines="warn", dtype=data_types, quotechar='"', encoding="utf-8")
ratings.rename(columns=ratings_new_col_names, inplace=True)
ratings = ratings[ratings['RATING']!=0]

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
existing_books = books["ISBN"]

ratings = ratings.query('ISBN in @existing_books')


print(ratings.describe)
ratings.to_csv("L1\\book_ratings_cleaned.csv", sep=";", quotechar='"', encoding="utf-8", index=False)
ratings = pd.read_csv("L1\\book_ratings_cleaned.csv", sep=";", on_bad_lines="warn", dtype=ratings_new_data_types, quotechar='"', encoding="utf-8")
print(ratings.describe())
print(ratings["RATING"].unique())