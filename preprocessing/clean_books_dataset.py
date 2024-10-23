import pandas as pd
import numpy as np

data_types = {
    "ISBN": "str",
    "Book-Title": "str",
    "Book-Author": "str",
    "Year-Of-Publication": "str",
    "Publisher": "str",
    "Image-URL-S": "str",
    "Image-URL-M": "str",
    "Image-URL-L": "str"
}

new_col_names = {
    "ISBN": "ISBN",
    "Book-Title": "TITLE",
    "Book-Author": "AUTHOR",
    "Year-Of-Publication": "PUBLICATION_YEAR",
    "Publisher": "PUBLISHER",
    "Image-URL-S": "IMAGE_URL_S",
    "Image-URL-M": "IMAGE_URL_M",
    "Image-URL-L": "IMAGE_URL_L"
}

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

# wouldnt raise an error in pd.read
forbidden_squences = [b"\xc3?\xc2?", b"\xc2?", b"\xc3?"]

with open("L1\\books_intermediary.csv", "w", encoding="utf-8") as out_file:
    pass

with open("L0\\BX-Books.csv", "rb") as file:
    lines = file.readlines()

with open("L1\\books_intermediary.csv", "a", encoding="utf-8") as out_file:
    for line in lines:
        for sequence, replacement_sequence in replacements.items(): 
            sequence_occurences = line.count(sequence)
            if sequence_occurences > 0:
                line = line.replace(sequence, replacement_sequence)
        if any(forbiden_sequence in line for forbiden_sequence in forbidden_squences):
            print("cant handle this sequence, too much data corruption")
            continue
        decoded_line = line.decode("utf-8")
        out_file.write(decoded_line)
        

books = pd.read_csv("L1\\books_intermediary.csv", sep=";", on_bad_lines="warn", dtype=data_types, quotechar='"', escapechar="\\", encoding="utf-8")
books.rename(columns=new_col_names, inplace=True)

books = books.drop(["IMAGE_URL_S", "IMAGE_URL_M", "IMAGE_URL_L"], axis=1)
cols = ["ISBN", "TITLE", "AUTHOR", "PUBLICATION_YEAR", "PUBLISHER"]
books = books[cols]
books = books.dropna()
books.to_csv("L1\\books_cleaned.csv", sep=";", quotechar='"', escapechar="\\", encoding="utf-8", na_rep=pd.NA, index=False, mode="w")
books = pd.read_csv("L1\\books_cleaned.csv", sep=";", on_bad_lines="warn", dtype=new_data_types, quotechar='"', escapechar="\\", encoding="utf-8")
print(books.describe())
