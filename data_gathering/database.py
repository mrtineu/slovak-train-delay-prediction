from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import os
import logging
logger = logging.getLogger(__name__)

load_dotenv()
CONNECTION_STRING = os.environ["MONGO_DB_URL"]

def get_database():
    client = MongoClient(CONNECTION_STRING)
    return client['TrainDelaysDB']

def save_snapshot(trains) -> bool:
    if not trains:
        logger.error("Input variable 'trains' is empty, so skipping saving snapshot")
        return False
    snapshot = {
        "timestamp" : datetime.now(),
        "train_count": len(trains),
        "trains" : trains
    }
    db= get_database()
    logger.debug("Saving snapshot to MongoDB")
    result = db['trainStateSnaphots'].insert_one(snapshot)
    if not result:
        logger.error(f"Snapshot(train_count={len(trains)}) was NOT saved to MongoDB")
    else:
        logger.info(f"Snapshot(train_count={len(trains)}) was saved to MongoDB")
    return result.acknowledged

