import pandas as pd
import csv
from datetime import datetime



# books outside of big 5 publishers
def publishers(df:pd.DataFrame):
    raise NotImplementedError()

    # Harper Collins vs HarperCollins... subsidiaries??

# books marked as to-read and read within 7 days
def impulse_reads(df:pd.DataFrame) -> pd.DataFrame:
    # df = df[df['Exclusive Shelf'] == 'read']
    cleaned = df.dropna(subset=['Date Read', 'Date Added']).copy()

    cleaned['Date Read'] = pd.to_datetime(cleaned['Date Read'], errors='coerce')
    cleaned['Date Added'] = pd.to_datetime(cleaned['Date Added'], errors='coerce')

    cleaned['Days Between'] = (cleaned['Date Read'] - cleaned['Date Added']).dt.days
    cleaned = cleaned[ (cleaned['Days Between'] <= 7) & (cleaned['Days Between'] > 1)] # more than 1 because not counting on that day or next day

    columns = ['Title', 'Author', 'Date Read', 'Date Added', 'Days Between']

    return cleaned.sort_values('Days Between')[columns] # should i bucketize or just return top 5?
    # difference in reader psychology for books finished in 1-3 days vs 4-7? should i focus on one or both


# books with largest gap between to-read and read that were highly rated by user
def sleeper_gem(df:pd.DataFrame) -> pd.DataFrame:
    # df = df[df['Exclusive Shelf'] == 'read']
    cleaned = df.dropna(subset=['Date Read', 'Date Added']).copy()

    cleaned['Date Read'] = pd.to_datetime(cleaned['Date Read'], errors='coerce')
    cleaned['Date Added'] = pd.to_datetime(cleaned['Date Added'], errors='coerce')

    cleaned['Days Between'] = (cleaned['Date Read'] - cleaned['Date Added']).dt.days
    columns = ['Title', 'Author', 'My Rating', 'Date Read', 'Date Added', 'Days Between']
    cleaned = cleaned[cleaned['My Rating'] > really_like(0.5, df)].sort_values('Days Between')[columns]

    cleaned = cleaned[cleaned['Days Between'] > 30] # i've decided that sleeper gems gotta be at least > 30 days..

    return cleaned

def really_like(value: int, df: pd.DataFrame) -> int:

    df = df.dropna(subset=['My Rating']).copy()

    return df['My Rating'].quantile(value)


# highest rated titles with fewest # of readers
def hidden_gem(df:pd.DataFrame):
    raise NotImplementedError()

# books read way past publication year that user reallllly liked
# is reallly liked above mean? 1std above mean?
# how late is late
def late_to_party(df:pd.DataFrame):
    raise NotImplementedError()

# longest streak of days where books logged as 'read'
def longest_binge_session(df: pd.DataFrame) -> pd.DataFrame:

    # df = df[df['Exclusive Shelf'] == 'read']
    df = df.dropna(subset=['Date Read']).copy()
    df['Date Read'] = pd.to_datetime(df['Date Read'], errors='coerce')
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


# trend setter vs adopter
# compare date read w peak popularity
def how_trendy(df: pd.DataFrame):
    raise NotImplementedError()

# df = pd.read_csv("my_reads.csv")
# print(longest_binge_session(df))