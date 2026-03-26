from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()
CONNECTION_STRING = os.environ["MONGO_DB_URL"]

def get_database():
    client = MongoClient(CONNECTION_STRING)
    return client['TrainDelaysDB']