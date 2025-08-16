from fastapi import FastAPI, File, UploadFile
import pandas as pd
import io
import csv
from io import StringIO
from app.calculations.totals import total_read, total_toread, total_pages, total_authors
from app.calculations.misc import impulse_reads, longest_binge_session, sleeper_gem


app = FastAPI()

@app.get("/")
def root():
    return {"message": "CSV microservice running"}

@app.post("/parse-csv")
async def parse_csv(file: UploadFile = File(...)):
    print("microservice")
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))
    read_df = clean_loaded_df(df)
    result = {
        "total_books": len(df),
        "total_read": total_read(df),
        "total_toread": total_toread(df),
        "total_pages": total_pages(read_df),
        "total_authors": total_authors(read_df),
        "impulse_reads": impulse_reads(read_df).to_json(orient="records", date_format="iso"),
        "longest_binge_session": longest_binge_session(read_df).to_json(orient="records", date_format="iso"),
        "sleeper_gem": sleeper_gem(read_df).to_json(orient="records", date_format="iso"),
    }
    return result

def clean_loaded_df(df: pd.DataFrame) -> pd.DataFrame:

    return df[df['Exclusive Shelf'] == 'read']


# add entire csv vs yearly review data logic here. no year parsing in helper functions