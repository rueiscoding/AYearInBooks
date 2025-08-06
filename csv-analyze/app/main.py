from fastapi import FastAPI, File, UploadFile
import pandas as pd
import io
import csv
from io import StringIO
from app.calculations.totals import total_read, total_toread, total_pages, total_authors


app = FastAPI()

@app.get("/")
def root():
    return {"message": "CSV microservice running"}

@app.post("/parse-csv")
async def parse_csv(file: UploadFile = File(...)):
    print("microservice")
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))
    result = {
        "total_books": len(df),
        "total_read": total_read(df),
        "total_toread": total_toread(df),
        "total_pages": total_pages(df),
        "total_authors": total_authors(df),
    }
    return result