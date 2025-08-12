import pandas as pd
import csv
from datetime import datetime



# books outside of big 5 publishers
def publishers(df:pd.DataFrame):
    raise NotImplementedError()

    # Harper Collins vs HarperCollins... subsidiaries??

# books marked as to-read and read within 7 days
def impulse_reads(df:pd.DataFrame) -> pd.DataFrame:
    df = df[df['Exclusive Shelf'] == 'read']
    cleaned = df.dropna(subset=['Date Read', 'Date Added'])

    cleaned['Date Read'] = pd.to_datetime(cleaned['Date Read'], errors='coerce')
    cleaned['Date Added'] = pd.to_datetime(cleaned['Date Added'], errors='coerce')

    cleaned['Days Between'] = (cleaned['Date Read'] - cleaned['Date Added']).dt.days
    cleaned = cleaned[ (cleaned['Days Between'] <= 7) & (cleaned['Days Between'] > 1)] # more than 1 because not counting on that day or next day

    columns = ['Title', 'Author', 'Date Read', 'Date Added', 'Days Between']
    return cleaned.sort_values('Days Between')[columns].head(5) # should i bucketize or just return top 5?
    # difference in reader psychology for books finished in 1-3 days vs 4-7? should i focus on one or both


# books with largest gap between to-read and read that were highly rated by user
def sleeper_gem(df:pd.DataFrame):
    raise NotImplementedError()

# highest rated titles with fewest # of readers
def hidden_gem(df:pd.DataFrame):
    raise NotImplementedError()

# books read way past publication year that user reallllly liked
# is reallly liked above mean? 1std above mean?
# how late is late
def late_to_party(df:pd.DataFrame):
    raise NotImplementedError()

# longest streak of days where books logged as 'read'
def longest_binge_session(df: pd.DataFrame):
    raise NotImplementedError()

# trend setter vs adopter
# compare date read w peak popularity
def how_trendy(df: pd.DataFrame):
    raise NotImplementedError()