import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGO_DB_URL = os.environ["MONGO_DB_URL"]
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "TrainDelaysDB")
COLLECTION_NAME = "trainStateSnaphots"


def get_database():
    client = MongoClient(MONGO_DB_URL)
    client.admin.command("ping")
    print(f"Connected to MongoDB database: {MONGO_DB_NAME}")
    return client[MONGO_DB_NAME]


db = get_database()
collection = db[COLLECTION_NAME]

print(collection.find_one())
