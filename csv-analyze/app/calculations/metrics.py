import pandas as pd
import csv
import os

# 'My Rating' and 'Average Rating' and 'Publisher' and 'Number of Pages' and 'Original Publication Year'

# oldest book read
def oldest_book(df: pd.DataFrame) -> pd.DataFrame:

    df = df[df['Exclusive Shelf'] == 'read']
    cleaned = df.dropna(subset='Original Publication Year')

    sorted = cleaned.sort_values('Original Publication Year')
    columns = ['Title', 'Author', 'Original Publication Year']

    return sorted[columns].head(5)


# user average rating vs goodreads average rating
def rating_averages(df: pd.DataFrame) -> tuple[int, int]:

    df = df[df['Exclusive Shelf'] == 'read']

    # can't decide which one to use
    user_average = df['My Rating'].mean()
    user_average_dropped_zeros = df[df['My Rating'] != 0]['My Rating'].mean()

    goodreads_average = df['Average Rating'].mean()
    return (round(user_average_dropped_zeros, 2), round(goodreads_average, 2))

# book with largest rating disparity
# most well received book that user rated poorly. 
# in future, take popularity into account for meaningful disagreements. use google books api
def largest_rating_disparity(df: pd.DataFrame) -> pd.DataFrame:
    
    df = df[ (df['Exclusive Shelf'] == 'read') & (df['My Rating'] != 0) ] # ignore zero ratings

    df['Rating Difference'] = abs(df['My Rating'].sub(df['Average Rating'], axis=0))
    sorted = df.sort_values('Rating Difference', ascending=False)

    columns = ['Title', 'Author', 'My Rating', 'Average Rating', 'Rating Difference']
    return sorted[columns].head(5)

def average_pages_per_book(df: pd.DataFrame) -> int:

    df = df[df['Exclusive Shelf'] == 'read']
    cleaned = df.dropna(subset='Number of Pages')
    return round(cleaned['Number of Pages'].mean())

def get_rating_quantile(df: pd.DataFrame, q: int) -> int:
    df = df[df['Exclusive Shelf'] == 'read']
    return df['My Rating'].quantile(q)