import os
import json
import logging
from datetime import datetime
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv
import asyncio


load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")


CHANNELS = [
    "lobelia4cosmetics",
    "tikvahpharma",
    "CheMed123"
]


RAW_DATA_PATH = "data/raw"
MESSAGE_PATH = os.path.join(RAW_DATA_PATH, "telegram_messages")
IMAGE_PATH = os.path.join(RAW_DATA_PATH, "images")
LOG_PATH = "logs"

os.makedirs(MESSAGE_PATH, exist_ok=True)
os.makedirs(IMAGE_PATH, exist_ok=True)
os.makedirs(LOG_PATH, exist_ok=True)


logging.basicConfig(
    filename=os.path.join(LOG_PATH, "scraper.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


client = TelegramClient("telegram_scraper_session", API_ID, API_HASH)


async def scrape_channel(channel_name: str):
    logging.info(f"Started scraping channel: {channel_name}")

    today = datetime.now().strftime("%Y-%m-%d")
    date_folder = os.path.join(MESSAGE_PATH, today)
    os.makedirs(date_folder, exist_ok=True)

    messages = []

    try:
        async for message in client.iter_messages(channel_name):
            record = {
                "message_id": message.id,
                "date": message.date.isoformat() if message.date else None,
                "text": message.text,
                "views": message.views,
                "forwards": message.forwards,
                "media": bool(message.media)
            }

            if isinstance(message.media, MessageMediaPhoto):
                channel_image_dir = os.path.join(IMAGE_PATH, channel_name)
                os.makedirs(channel_image_dir, exist_ok=True)

                image_file = os.path.join(channel_image_dir, f"{message.id}.jpg")
                await message.download_media(file=image_file)
                record["image_path"] = image_file

            messages.append(record)


        output_file = os.path.join(date_folder, f"{channel_name}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)

        logging.info(f"Finished scraping channel: {channel_name}")

    except Exception as e:
        logging.error(f"Error scraping channel {channel_name}: {str(e)}")


async def main():
    for channel in CHANNELS:
        await scrape_channel(channel)

async def run_scraper():
    await client.start()   
    await main()

asyncio.run(run_scraper())
