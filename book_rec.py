# import
import pandas as pd
import numpy as np
from typing import List

#TODO replace with database
book_ratings = pd.read_csv("L1\\merged.csv", sep=";", on_bad_lines="warn", quotechar='"', encoding="utf-8")

input_book = 'the fellowship of the ring (the lord of the rings, part 1)'

def get_readers_of_book(input_book: str) -> List:
    readers = book_ratings['USER_ID'][(book_ratings['TITLE_LOWERCASE']==input_book)]
    readers = readers.tolist()
    readers = np.unique(readers)
    return readers

def get_books_ranked_by_readers(readers: List, rank_count_threshold: int) -> pd.DataFrame:
    books_of_readers = book_ratings[(book_ratings['USER_ID'].isin(readers))]
    
    number_of_rating_per_book = books_of_readers.groupby(['TITLE_LOWERCASE']).agg('count').reset_index()
    
    #select only books which have actually higher number of ratings than threshold
    books_to_compare = number_of_rating_per_book['TITLE_LOWERCASE'][number_of_rating_per_book['USER_ID'] >= rank_count_threshold]
    books_to_compare = books_to_compare.tolist()
    ratings_book_to_compare = books_of_readers[['USER_ID', 'RATING', 'TITLE_LOWERCASE']][books_of_readers['TITLE_LOWERCASE'].isin(books_to_compare)]

    return ratings_book_to_compare

def get_ratings_per_user_and_book(ratings_book_to_compare: pd.DataFrame) -> pd.DataFrame:
    # group by User and Book and compute mean
    ratings_per_user_and_book = ratings_book_to_compare.groupby(['USER_ID', 'TITLE_LOWERCASE'])['RATING'].mean()

    # reset index to see User-ID in every row
    ratings_per_user_and_book = ratings_per_user_and_book.to_frame().reset_index()

    return ratings_per_user_and_book

def get_correlation_dataset(ratings_per_user_and_book: pd.DataFrame) -> pd.DataFrame:
    correlation_dataset = ratings_per_user_and_book.pivot(index='USER_ID', columns='TITLE_LOWERCASE', values='RATING')
    return correlation_dataset

def get_books_correlation(correlation_dataset: pd.DataFrame) -> pd.Series:  
    correlation_dataset.corr()
    input_book_correlations = correlation_dataset.corr()[input_book]
    input_book_correlations = input_book_correlations.rename("correlation")

    return input_book_correlations

def get_books_average_rating(correlation_dataset: pd.DataFrame) -> pd.Series:
    input_book_averages = correlation_dataset.mean()
    input_book_averages = input_book_averages.rename("average")

    return input_book_averages

def get_final_dataset(input_book_correlations: pd.Series, input_book_averages: pd.Series, n: int=10) -> pd.DataFrame:
    values = pd.concat([input_book_averages, input_book_correlations], axis=1).reset_index()
    #TODO all search logic should be done using IBAN, otherwise we will run into problems the moment queried book title a) exists multiple times b) is also recommended
    values = values[values["TITLE_LOWERCASE"] != input_book]
    values = values.sort_values('correlation', ascending = False).head(n)
    print(values)

readers = get_readers_of_book(input_book=input_book)
ratings_book_to_compare = get_books_ranked_by_readers(readers=readers, rank_count_threshold=8)
ratings_per_user_and_book = get_ratings_per_user_and_book(ratings_book_to_compare)
correlation_dataset = get_correlation_dataset(ratings_per_user_and_book)
input_book_correlations = get_books_correlation(correlation_dataset=correlation_dataset)
input_book_averages= get_books_average_rating(correlation_dataset=correlation_dataset)
result = get_final_dataset(input_book_correlations, input_book_averages)