import pandas as pd

# books read: check 'Exclusive Shelf' for 'read'
def total_read(df: pd.DataFrame) -> int:
    
    counts = df['Exclusive Shelf'].value_counts()
    return counts['read']


# books in to-read: check 'Exclusive Shelf' for 'to-read'
def total_toread(df: pd.DataFrame) -> int:

    counts = df['Exclusive Shelf'].value_counts()
    return counts['to-read']

# pages read: if 'Exclusive Shelf' is 'read', sum values in 'Number of Pages'
def total_pages(df: pd.DataFrame) -> int:

    total = 0
    filtered = df.dropna(subset=['Number of Pages'])
    filtered = filtered[filtered['Exclusive Shelf'] == 'read']

    for index, row in filtered.iterrows():
        total += row['Number of Pages']

    return total

# unique authors read: check 'Author' and if 'Exclusive Shelf' is 'read'
def total_authors(df: pd.DataFrame) -> int:

    filtered = df[df['Exclusive Shelf'] == 'read']
    return filtered['Author'].nunique()


