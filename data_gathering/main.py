import parser
import database
import scrape
import time
import discord
import logging
from dotenv import load_dotenv
import os 

load_dotenv()
#In seconds
DELAY_BETWEEN_REQUESTS = int(os.environ["DELAY_BETWEEN_REQUESTS"])
ENABLE_DISCORD_WEBHOOK = os.environ["ENABLE_DISCORD_WEBHOOK"]

logging.basicConfig(filename="log.log", level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def main():
    while True:
        data = scrape.get_train_state()
        if not data:
            logger.error(f"Data recieved from API are empty")
            if(ENABLE_DISCORD_WEBHOOK):
                discord.discord_log("Data recieved are empty from the API")            
            time.sleep(DELAY_BETWEEN_REQUESTS)
            continue
        clean_data = parser.clean_train_data(data)
        result = database.save_snapshot(clean_data)
        if not result:
            logger.error("Write to MongoDB failed and snapshot is not saved")
            if ENABLE_DISCORD_WEBHOOK:
                discord.discord_log("Write to MongoDB failed and snapshot is not saved")
        else:
            logger.info("Snapshot has been succsefuly saved and contiouing to sleep")
            if ENABLE_DISCORD_WEBHOOK:
                discord.discord_log(f"Snapshot({len(clean_data)}) has been succsefuly saved and contiouing to sleep")
        time.sleep(DELAY_BETWEEN_REQUESTS)
        



if __name__ == "__main__":
    main()
