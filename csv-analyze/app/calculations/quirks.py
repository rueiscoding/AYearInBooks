import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()

GB_KEY = os.getenv("GBOOKS_KEY")

# unfortunately, google books is not comparable to goodreads in terms of scale. gb ratings count
# is in the few hundreds even for mega bestsellers... 

# highest rated titles with fewest # of readers
def hidden_gem(df:pd.DataFrame):
    raise NotImplementedError()

# books read way past publication year that user reallllly liked
# is reallly liked above mean? 1std above mean?
# how late is late
def late_to_party(df:pd.DataFrame):
    raise NotImplementedError()


# trend setter vs adopter
# compare date read w peak popularity
def how_trendy(df: pd.DataFrame):
    raise NotImplementedError()