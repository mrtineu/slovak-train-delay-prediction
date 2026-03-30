from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_DB_URL = os.environ["MONGO_DB_URL"]

def get_database():
    client = MongoClient(MONGO_DB_URL)
    print("Connected to MongoDB")
    client.admin.command('ping')
    # Print info about the MongoDB server
    print("MongoDB server info:", client.server_info())
    # Print the names of the databases in the MongoDB server
    print("Databases in MongoDB server:", client.list_database_names())
    return client['trainStateSnaphots']

print(MONGO_DB_URL)

db = get_database()

collection = db['trainStateSnaphots']

print(collection.find_one())