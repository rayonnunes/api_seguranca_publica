import os
from os.path import join, dirname
from dotenv import load_dotenv
import pymongo

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def connect_mongo():
    mongo_uri = os.environ.get("MONGO_URI")
    client = pymongo.MongoClient(mongo_uri)
    db = client.base_sinesp
    collection = db.registros
    return collection
