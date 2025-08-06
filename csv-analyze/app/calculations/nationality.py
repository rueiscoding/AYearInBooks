import pandas as pd
from pymongo import MongoClient
from pymongo.collection import Collection
import os
import requests
import csv
from collections import Counter
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "Wrapped"
COLLECTION_NAME = "Nationality"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
author_collection: Collection = db[COLLECTION_NAME]

# getting nationality of authors
def around_world(df: pd.DataFrame) -> None:
    world_map = {}

    df = df[df['Exclusive Shelf'] == 'read']
    df = df.sample(1)

    for index, row in df.iterrows():
        author = row['Author'] # need method to normalize name. spaces between first n last
        title = row['Title']

        country = check_db(author.strip().lower())
        print(author)
        print(country)

        if not country:
            country = call_open_library_api(author)
            doc = {"author": author.lower(), "country" : country} #insert author lowered
            author_collection.insert_one(doc)

        # if counry is None then don't include in stats. not a bug.
        if country != 'None':
            if country not in world_map:
                world_map[country] = []
            world_map[country].append((author, title)) #when building, author title capitalized
    
    print("\n\n world map")
    print(world_map)


def check_db(author_name: str) -> str | None:
    doc = author_collection.find_one({'author': author_name})
    if doc:
        # print(doc)
        return doc.get('country')
    return None
    
def call_open_library_api(author_name:str) -> str:
    base = "https://openlibrary.org/search/authors.json"
    # https://openlibrary.org/search/authors.json?q=Chinua%20Achebe
    params = {"q": author_name}
    response = requests.get(base, params=params)

    if response.status_code == 200:
        data = response.json()

        top_subjects_list = []
        documents = data['docs']
        for doc in documents:
            if 'top_subjects' in doc:
                top_subjects_list.extend(doc["top_subjects"])

        return nationality_from_list(top_subjects_list)
    else:
        print("failed to fetch")
        return "None"

def nationality_from_list(subjects: list) -> str:
    print(subjects)

    matches = []

    with open('country_dict.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
    
    if 'Translations into English' in subjects: # so we dont match to UK accidentally.
        subjects.remove('Translations into English')
    
    for val in subjects:
        words = val.lower().split() # Italian Literature --> Italian, Literature
        for row in rows:

            nat = row['nationality'].lower()
            country = row['country'].lower()

            if val.lower() == nat or val.lower()==country: # to match United States, for example. match exact words
                matches.append(row['country'])
            
            #if we couldnt get exact match
            elif any((word == nat or word == country) for word in words): # check each word in subjects
                matches.append(row['country'])
    

    # if has "____ literature" should ignore UK and US as origin?

    print(matches)
    if len(matches) == 0:
        return "None"

    freq_map = Counter(matches)
    # print(freq_map.most_common(1)[0][0])
    return freq_map.most_common(1)[0][0]



    

df = pd.read_csv('my_reads.csv')
around_world(df)




# if author in database, get country of origin

# else, call open library api
# compare elements in "top_subjects" to csv of nationality, country dict
# get country and save to database

# return{country: country name, books: {book, author}

# translators/editors like robert chandler will be mapped to Russia instead of UK.
# even though origin is not Russia, if you are reading Robert Chandler, most likely some russian translated into english

# camus as french

# Pam Muñoz Ryan as mexican