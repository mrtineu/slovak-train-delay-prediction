from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
load_dotenv()
CONNECTION_STRING = os.environ["MONGO_DB_URL"]

def get_database():
    client = MongoClient(CONNECTION_STRING)
    return client['TrainDelaysDB']


def get_recent_online_trains(collection, minutes: int) -> list[dict]:
    cutoff = datetime.now() - timedelta(minutes=minutes)
    pipeline = [
        {"$match": {"timestamp": {"$gte": cutoff}}},
        {"$unwind": "$trains"},
        {
            "$group": {
                "_id": "$trains.CisloVlaku",
                "last_seen_online_at": {"$max": "$timestamp"},
                "train_name": {"$last": "$trains.NazovVlaku"},
                "train_type": {"$last": "$trains.TypVlaku"},
            }
        },
        {"$sort": {"last_seen_online_at": -1}},
    ]
    return [
        {
            "train_number": doc["_id"],
            "last_seen_online_at": doc["last_seen_online_at"],
            "train_name": doc.get("train_name"),
            "train_type": doc.get("train_type"),
        }
        for doc in collection.aggregate(pipeline)
        if doc.get("_id")
    ]


def get_cached_train_numbers(collection) -> set[str]:
    return {
        doc["train_number"]
        for doc in collection.find({}, {"train_number": 1, "_id": 0})
        if doc.get("train_number")
    }


def can_request_train(collection, train: dict, now: datetime) -> bool:
    state = collection.find_one({"train_number": train["train_number"]})
    if not state:
        return True
    previous_seen = state.get("last_seen_online_at")
    if previous_seen and train["last_seen_online_at"] and train["last_seen_online_at"] > previous_seen:
        return True
    cooldown_until = state.get("cooldown_until")
    return not cooldown_until or cooldown_until <= now


def save_timetable(collection, train: dict, stops: list[str]) -> None:
    now = datetime.now()
    collection.update_one(
        {"train_number": train["train_number"]},
        {
            "$set": {
                "stops": stops,
                "stops_count": len(stops),
                "last_success_at": now,
                "last_seen_online_at": train["last_seen_online_at"],
                "train_name": train.get("train_name"),
                "train_type": train.get("train_type"),
            },
            "$setOnInsert": {
                "first_success_at": now,
            },
        },
        upsert=True,
    )


def save_request_result(collection, train: dict, result: str, cooldown_minutes: int) -> None:
    now = datetime.now()
    existing = collection.find_one({"train_number": train["train_number"]}) or {}
    fail_count = 0 if result == "success" else existing.get("fail_count", 0) + 1
    cooldown_until = None if result == "success" else now + timedelta(minutes=cooldown_minutes)
    collection.update_one(
        {"train_number": train["train_number"]},
        {
            "$set": {
                "last_attempt_at": now,
                "last_result": result,
                "fail_count": fail_count,
                "cooldown_until": cooldown_until,
                "last_seen_online_at": train["last_seen_online_at"],
            }
        },
        upsert=True,
    )