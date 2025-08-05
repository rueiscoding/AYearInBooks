from fastapi import FastAPI, File, UploadFile
import pandas as pd
import io
import csv
from io import StringIO


app = FastAPI()

@app.get("/")
def root():
    return {"message": "CSV microservice running"}

@app.post("/parse-csv")
async def parse_csv(file: UploadFile = File(...)):
    print("microservice")
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))
    return {"total_rows": len(df)}