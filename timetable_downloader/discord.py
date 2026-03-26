from discord_webhook import DiscordWebhook
import logging
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()


def discord_log(msg: str):
    discord_webhook = os.environ.get("DISCORD_WEBHOOK")
    if not discord_webhook:
        logger.error("DISCORD_WEBHOOK is not set")
        return
    webhook = DiscordWebhook(discord_webhook, content=msg)
    try:
        response = webhook.execute()
        if not response.ok:
            logger.error(f"Discord webhook response has not been successful, status code {response.status_code}")
    except Exception as e:
        logger.error(f"Discord webhook has not been sent sucsefully: {e}")