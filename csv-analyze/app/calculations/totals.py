import pandas as pd

# books read: check 'Exclusive Shelf' for 'read'
def total_read(df: pd.DataFrame) -> int:
    
    counts = df['Exclusive Shelf'].value_counts()
    return int(counts['read'])


# books in to-read: check 'Exclusive Shelf' for 'to-read'
def total_toread(df: pd.DataFrame) -> int:

    counts = df['Exclusive Shelf'].value_counts()
    return int(counts['to-read'])

# pages read: sum values in 'Number of Pages'
def total_pages(df: pd.DataFrame) -> int:

    total = 0
    filtered = df.dropna(subset=['Number of Pages'])

    for index, row in filtered.iterrows():
        total += row['Number of Pages']

    return int(total)

# unique authors read: check 'Author'
def total_authors(df: pd.DataFrame) -> int:

    return int(df['Author'].nunique())


