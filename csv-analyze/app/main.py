from fastapi import FastAPI, File, UploadFile
import pandas as pd
import io
import csv
from io import StringIO
from datetime import datetime
from app.calculations.totals import total_read, total_toread, total_pages, total_authors
from app.calculations.misc import impulse_reads, longest_binge_session, sleeper_gem, indie_titles, biggest_book_slump, fomo_count, number_of_reviews
from app.calculations.metrics import oldest_book, rating_averages, largest_rating_disparity, average_pages_per_book


app = FastAPI()

@app.get("/")
def root():
    return {"message": "CSV microservice running"}

@app.post("/parse-csv")
async def parse_csv(file: UploadFile = File(...)):
    print("microservice")
    contents = await file.read()
    raw_csv = pd.read_csv(io.BytesIO(contents))

    all_years = all_time_df(raw_csv) 
    df = current_year(all_years)    # to-read and read books from current year
    read_df = read_books(df)    # only read books from current year

    result = {
        # foundational stats
        "total_books": len(df),
        "total_read": total_read(df),
        "total_toread": total_toread(df), # books marked as toread
        "total_pages": total_pages(read_df), # total pages read
        "total_authors": total_authors(read_df),
        "oldest_book": oldest_book(read_df),

        # taste and quirk
        "largest_rating_difference": largest_rating_disparity(read_df).to_json(orient="records"),
        "user_vs_goodreads": rating_averages(read_df),
        "impulse_reads": impulse_reads(read_df).to_json(orient="records", date_format="iso"),
        "sleeper_gem": sleeper_gem(read_df).to_json(orient="records", date_format="iso"),
        "indie_titles": indie_titles(read_df),
        "fomo_count": fomo_count(read_df),

        # # reading journey
        "longest_binge_session": longest_binge_session(read_df).to_json(orient="records", date_format="iso"),
        "longest_book_slump": biggest_book_slump(read_df).to_json(orient="records", date_format="iso"),
        "reviewer_or_lurker": number_of_reviews(read_df),
    }

    return result

def all_time_df(df: pd.DataFrame) -> pd.DataFrame:

    df['Original Publication Year'] = pd.to_numeric(df['Original Publication Year'], errors='coerce')
    df['Date Read'] = pd.to_datetime(df['Date Read'], errors='coerce')
    df['Date Added'] = pd.to_datetime(df['Date Added'], errors='coerce')

    return df


def current_year(df: pd.DataFrame) -> pd.DataFrame:

    current_datetime = datetime.now()
    current_month = current_datetime.month
    current_year = current_datetime.year

    if current_month < 6:
        current_year -=1
    
    # return books read in current year: df['Exclusive Shelf'] == 'read' and 'Date Read' is in current year
    # return books marked as to-read in current year: df['Exclusive Shelf'] == 'to-read' and 'Date Added' is in current year
    read_mask = ((df['Exclusive Shelf'] == 'read') & (df['Date Read'].dt.year == current_year))

    to_read_mask = ((df['Exclusive Shelf'] == 'to-read') & (df['Date Added'].dt.year == datetime.now().year))

    filtered_df = df[read_mask | to_read_mask].copy()

    return filtered_df

def read_books(df: pd.DataFrame) -> pd.DataFrame:

    return df[df['Exclusive Shelf'] == 'read']


# add entire csv vs yearly review data logic here. no year parsing in helper functions