from datetime import datetime
import logging
import os
import time

from database import (
    can_request_train,
    get_cached_train_numbers,
    get_database,
    get_recent_online_trains,
    save_request_result,
    save_timetable,
)
import discord
from dotenv import load_dotenv
from scrape import scrape_timetable


load_dotenv()
ENABLE_DISCORD_WEBHOOK = os.environ.get("ENABLE_DISCORD_WEBHOOK", "false").lower() == "true"
DELAY_BETWEEN_REQUESTS = int(os.environ.get("DELAY_BETWEEN_REQUESTS", "60"))

logging.basicConfig(filename="log.log", level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


RECENT_MINUTES = 30
FAILURE_COOLDOWN_MINUTES = 30
MAX_TRAINS_PER_RUN = 100


def main():
    while True:
        try:
            run_once()
        except Exception as e:
            logger.error(f"Timetable downloader cycle failed: {e}")
            if ENABLE_DISCORD_WEBHOOK:
                discord.discord_log(f"Timetable downloader cycle failed: {e}")
        time.sleep(DELAY_BETWEEN_REQUESTS)


def run_once():
    db = get_database()
    snapshots = db["trainStateSnaphots"]
    timetables = db["trainTimetables"]
    requests = db["trainTimetableRequests"]

    now = datetime.now()
    recent_online = get_recent_online_trains(snapshots, RECENT_MINUTES)
    cached_train_numbers = get_cached_train_numbers(timetables)

    candidates = []
    for train in recent_online:
        if train["train_number"] in cached_train_numbers:
            continue
        if not can_request_train(requests, train, now):
            continue
        candidates.append(train)
        if len(candidates) >= MAX_TRAINS_PER_RUN:
            break

    logger.info(f"recent_online={len(recent_online)} cached={len(cached_train_numbers)} candidates={len(candidates)}")
    print(f"recent_online={len(recent_online)} cached={len(cached_train_numbers)} candidates={len(candidates)}")
    if ENABLE_DISCORD_WEBHOOK and candidates:
        discord.discord_log(f"Timetable downloader found {len(candidates)} candidates from {len(recent_online)} recent online trains")

    for train in candidates:
        try:
            stops = scrape_timetable(train["train_number"])
        except Exception:
            save_request_result(requests, train, "error", FAILURE_COOLDOWN_MINUTES)
            logger.error(f"Train {train['train_number']} failed while downloading timetable")
            if ENABLE_DISCORD_WEBHOOK:
                discord.discord_log(f"Train {train['train_number']} failed while downloading timetable")
            print(f"{train['train_number']}: error")
            continue

        if stops:
            save_timetable(timetables, train, stops)
            save_request_result(requests, train, "success", FAILURE_COOLDOWN_MINUTES)
            logger.info(f"Train {train['train_number']} saved with {len(stops)} stops")
            if ENABLE_DISCORD_WEBHOOK:
                discord.discord_log(f"Train {train['train_number']} saved with {len(stops)} stops")
            print(f"{train['train_number']}: saved {len(stops)}")
        else:
            save_request_result(requests, train, "empty", FAILURE_COOLDOWN_MINUTES)
            logger.error(f"Train {train['train_number']} returned empty timetable")
            if ENABLE_DISCORD_WEBHOOK:
                discord.discord_log(f"Train {train['train_number']} returned empty timetable")
            print(f"{train['train_number']}: empty")

if __name__ == "__main__":
    main()
