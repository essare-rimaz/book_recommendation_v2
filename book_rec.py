# import
import pandas as pd
import numpy as np

book_ratings = pd.read_csv("L1\\merged.csv", sep=";", on_bad_lines="warn", quotechar='"', encoding="utf-8")

input_book = 'the fellowship of the ring (the lord of the rings, part 1)'
readers = book_ratings['USER_ID'][(book_ratings['TITLE_LOWERCASE']==input_book)]
readers = readers.tolist()
readers = np.unique(readers)

# final dataset
books_of_readers = book_ratings[(book_ratings['USER_ID'].isin(readers))]

# Number of ratings per other books in dataset
number_of_rating_per_book = books_of_readers.groupby(['TITLE_LOWERCASE']).agg('count').reset_index()

#select only books which have actually higher number of ratings than threshold
books_to_compare = number_of_rating_per_book['TITLE_LOWERCASE'][number_of_rating_per_book['USER_ID'] >= 8]
books_to_compare = books_to_compare.tolist()

ratings_book_to_compare = books_of_readers[['USER_ID', 'RATING', 'TITLE_LOWERCASE']][books_of_readers['TITLE_LOWERCASE'].isin(books_to_compare)]

# group by User and Book and compute mean
ratings_per_user_and_book = ratings_book_to_compare.groupby(['USER_ID', 'TITLE_LOWERCASE'])['RATING'].mean()

# reset index to see User-ID in every row
ratings_per_user_and_book = ratings_per_user_and_book.to_frame().reset_index()

correlation_dataset = ratings_per_user_and_book.pivot(index='USER_ID', columns='TITLE_LOWERCASE', values='RATING')
   
correlation_dataset.corr()
input_book_correlations = correlation_dataset.corr()[input_book]
input_book_correlations = input_book_correlations.rename("correlation")

averages = correlation_dataset.mean()
averages = averages.rename("average")

values = pd.concat([averages, input_book_correlations], axis=1).reset_index()
#TODO all search logic should be done using IBAN, otherwise we will run into problems the moment queried book title a) exists multiple times b) is also recommended
values = values[values["TITLE_LOWERCASE"] != input_book]
values = values.sort_values('correlation', ascending = False).head(10)
print(values)