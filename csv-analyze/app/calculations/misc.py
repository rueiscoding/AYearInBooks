import pandas as pd
import csv
import os
from datetime import datetime



# books outside of big 5 publishers
# publisher_dict has gotta be exhaustive for this to work
# counts subsidiaries and imprints as non indie
def indie_titles(df:pd.DataFrame):
    # df = df[df['Exclusive Shelf'] == 'read']

    here = os.path.dirname(__file__)
    csv_path = os.path.join(here, "publisher_dict.csv")
    big_5 = pd.read_csv(csv_path)

    big5_aliases = set(big_5['alias'].str.lower())
    df = df.dropna(subset=['Publisher']).copy()
    df['Publisher'] = df['Publisher'].str.lower().str.strip().replace(r'[^a-z\s]', '', regex=True)
    df['Publisher'] = (df['Publisher'].fillna('').str.lower().str.strip().str.replace(r'\s+', ' ', regex=True))
    
    def is_big5(publisher):
        return any(alias in publisher for alias in big5_aliases)

    df['IsBig5'] = df['Publisher'].apply(is_big5)

    indie_df = df[~df['IsBig5']]

    columns = ['Title', 'Publisher']

    number_unique = indie_df['Publisher'].nunique()

    # return indie_df[columns].sample(15)
    # return number_unique
    return len(indie_df)


# books marked as to-read and read within 7 days
def impulse_reads(df:pd.DataFrame) -> pd.DataFrame:
    # df = df[df['Exclusive Shelf'] == 'read']
    cleaned = df.dropna(subset=['Date Read', 'Date Added']).copy()

    # cleaned['Date Read'] = pd.to_datetime(cleaned['Date Read'], errors='coerce')
    # cleaned['Date Added'] = pd.to_datetime(cleaned['Date Added'], errors='coerce')

    cleaned['Days Between'] = (cleaned['Date Read'] - cleaned['Date Added']).dt.days
    cleaned = cleaned[ (cleaned['Days Between'] <= 7) & (cleaned['Days Between'] > 1)] # more than 1 because not counting on that day or next day

    columns = ['Title', 'Author', 'Date Read', 'Date Added', 'Days Between']

    return cleaned.sort_values('Days Between')[columns] # should i bucketize or just return top 5?
    # difference in reader psychology for books finished in 1-3 days vs 4-7? should i focus on one or both


# books with largest gap between to-read and read that were highly rated by user
def sleeper_gem(df:pd.DataFrame) -> pd.DataFrame:
    # df = df[df['Exclusive Shelf'] == 'read']
    cleaned = df.dropna(subset=['Date Read', 'Date Added']).copy()

    # cleaned['Date Read'] = pd.to_datetime(cleaned['Date Read'], errors='coerce')
    # cleaned['Date Added'] = pd.to_datetime(cleaned['Date Added'], errors='coerce')

    cleaned['Days Between'] = (cleaned['Date Read'] - cleaned['Date Added']).dt.days
    columns = ['Title', 'Author', 'My Rating', 'Date Read', 'Date Added', 'Days Between']
    cleaned = cleaned[cleaned['My Rating'] > really_like(0.5, df)].sort_values('Days Between')[columns]

    cleaned = cleaned[cleaned['Days Between'] > 30] # i've decided that sleeper gems gotta be at least > 30 days..

    return cleaned

def really_like(value: int, df: pd.DataFrame) -> int:

    df = df.dropna(subset=['My Rating']).copy()

    return df['My Rating'].quantile(value)


# longest streak of days where books logged as 'read'
def longest_binge_session(df: pd.DataFrame) -> pd.DataFrame:

    # df = df[df['Exclusive Shelf'] == 'read']
    df = df.dropna(subset=['Date Read']).copy()
    # df['Date Read'] = pd.to_datetime(df['Date Read'], errors='coerce')
    df['Read Day'] = df['Date Read'].dt.normalize() # get rid of time

    unique_days = pd.Series(sorted(df['Read Day'].unique())) # sort n group unique days
    streak_groups = (unique_days.diff().dt.days != 1).cumsum()

    streak_lengths = streak_groups.value_counts()
    longest = streak_lengths.idxmax()
    streak_len = streak_lengths.max()

    if streak_len < 2:
        return pd.DataFrame()

    streak_days = unique_days[streak_groups == longest] # days in the streak

    streak_books = df[df['Read Day'].isin(streak_days)]
    streak_books = streak_books[['Title', 'Author', 'Date Read']].sort_values('Date Read')

    return streak_books

# longest went without reading a book
def biggest_book_slump(df: pd.DataFrame) -> pd.DataFrame:
    # df = df[df['Exclusive Shelf'] == 'read'] #jsut for  testing
    df = df.dropna(subset='Date Read')
    # df['Date Read'] = pd.to_datetime(df['Date Read'], errors='coerce')
    # df = df[df['Date Read'] > pd.Timestamp('2016-7-01')] #for testing

    sorted = df.sort_values('Date Read').reset_index(drop=True)
    sorted['Gap'] = sorted['Date Read'].diff()

    max_gap_idx = sorted['Gap'].idxmax() # row w largest gap
    columns = ['Title', 'Author', 'Date Read', 'Gap']

    return sorted.loc[[max_gap_idx - 1, max_gap_idx]][columns]
    # return sorted.head(10)[columns]

# when original publication year matches the date read
# allow year to be parameter
def fomo_count(df: pd.DataFrame) -> int:

    # df = df[df['Exclusive Shelf'] == 'read'] #jsut for  testing
    df = df.dropna(subset='Original Publication Year')
    df = df.dropna(subset='Date Read')

    # df['Date Read'] = pd.to_datetime(df['Date Read'], errors='coerce')
    df['Year Read'] = df['Date Read'].dt.year

    df = df[df['Original Publication Year'] == df['Year Read']]

    return len(df)

def number_of_reviews(df:pd.DataFrame) -> int:

    df = df.dropna(subset='My Review')

    return len(df)


# df = pd.read_csv("my_reads.csv")
# print(fomo_count(df))
