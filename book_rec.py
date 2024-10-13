# import
import pandas as pd
import numpy as np

# load ratings
ratings = pd.read_csv('L0\\BX-Book-Ratings.csv', encoding='cp1251', sep=';')
ratings = ratings[ratings['Book-Rating']!=0]

# load books
books = pd.read_csv('L0\\BX-Books.csv',  encoding='cp1251', sep=';',on_bad_lines="skip")

#users_ratigs = pd.merge(ratings, users, on=['User-ID'])
dataset = pd.merge(ratings, books, on=['ISBN'])
dataset_lowercase=dataset.apply(lambda x: x.str.lower() if(x.dtype == 'object') else x)

input_book = 'the fellowship of the ring (the lord of the rings, part 1)'
readers = dataset_lowercase['User-ID'][(dataset_lowercase['Book-Title']==input_book)]
readers = readers.tolist()
readers = np.unique(readers)

# final dataset
books_of_readers = dataset_lowercase[(dataset_lowercase['User-ID'].isin(readers))]

# Number of ratings per other books in dataset
number_of_rating_per_book = books_of_readers.groupby(['Book-Title']).agg('count').reset_index()

#select only books which have actually higher number of ratings than threshold
books_to_compare = number_of_rating_per_book['Book-Title'][number_of_rating_per_book['User-ID'] >= 8]
books_to_compare = books_to_compare.tolist()

ratings_book_to_compare = books_of_readers[['User-ID', 'Book-Rating', 'Book-Title']][books_of_readers['Book-Title'].isin(books_to_compare)]

# group by User and Book and compute mean
ratings_per_user_and_book = ratings_book_to_compare.groupby(['User-ID', 'Book-Title'])['Book-Rating'].mean()

# reset index to see User-ID in every row
ratings_per_user_and_book = ratings_per_user_and_book.to_frame().reset_index()

correlation_dataset = ratings_per_user_and_book.pivot(index='User-ID', columns='Book-Title', values='Book-Rating')
   
correlation_dataset.corr()
input_book_correlations = correlation_dataset.corr()[input_book]
input_book_correlations = input_book_correlations.rename("correlation")

averages = correlation_dataset.mean()
averages = averages.rename("average")

values = pd.concat([averages, input_book_correlations], axis=1).reset_index()
#TODO all search logic should be done using IBAN, otherwise we will run into problems the moment queried book title a) exists multiple times b) is also recommended
values = values[values["Book-Title"] != input_book]
values = values.sort_values('correlation', ascending = False).head(10)
print(values)