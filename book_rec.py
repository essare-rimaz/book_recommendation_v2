# import
import pandas as pd
import numpy as np

# load ratings
ratings = pd.read_csv('Downloads/BX-Book-Ratings.csv', encoding='cp1251', sep=';')
ratings = ratings[ratings['Book-Rating']!=0]

# load books
books = pd.read_csv('Downloads/BX-Books.csv',  encoding='cp1251', sep=';',error_bad_lines=False)

#users_ratigs = pd.merge(ratings, users, on=['User-ID'])
dataset = pd.merge(ratings, books, on=['ISBN'])
dataset_lowercase=dataset.apply(lambda x: x.str.lower() if(x.dtype == 'object') else x)

LoR_book = 'the fellowship of the ring (the lord of the rings, part 1)'
tolkien_readers = dataset_lowercase['User-ID'][(dataset_lowercase['Book-Title']==LoR_book) & (dataset_lowercase['Book-Author'].str.contains("tolkien"))]
tolkien_readers = tolkien_readers.tolist()
tolkien_readers = np.unique(tolkien_readers)

# final dataset
books_of_tolkien_readers = dataset_lowercase[(dataset_lowercase['User-ID'].isin(tolkien_readers))]

# Number of ratings per other books in dataset
number_of_rating_per_book = books_of_tolkien_readers.groupby(['Book-Title']).agg('count').reset_index()

#select only books which have actually higher number of ratings than threshold
books_to_compare = number_of_rating_per_book['Book-Title'][number_of_rating_per_book['User-ID'] >= 8]
books_to_compare = books_to_compare.tolist()

ratings_data_raw = books_of_tolkien_readers[['User-ID', 'Book-Rating', 'Book-Title']][books_of_tolkien_readers['Book-Title'].isin(books_to_compare)]

# group by User and Book and compute mean
ratings_data_raw_nodup = ratings_data_raw.groupby(['User-ID', 'Book-Title'])['Book-Rating'].mean()

# reset index to see User-ID in every row
ratings_data_raw_nodup = ratings_data_raw_nodup.to_frame().reset_index()

dataset_for_corr = ratings_data_raw_nodup.pivot(index='User-ID', columns='Book-Title', values='Book-Rating')
   
dataset_for_corr.corr()
correlations = dataset_for_corr.corr()[LoR_book]
correlations = correlations.rename("correlation")

averages = dataset_for_corr.mean()
averages = averages.rename("average")

values = pd.concat([averages, correlations], axis=1).reset_index()
#TODO all search logic should be done using IBAN, otherwise we will run into problems the moment queried book title a) exists multiple times b) is also recommended
values = values[values["Book-Title"] != LoR_book]
values = values.sort_values('correlation', ascending = False).head(10)
print(values)