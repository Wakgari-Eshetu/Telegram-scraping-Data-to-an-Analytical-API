import os
import json
import psycopg2
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATA_DIR = Path("data/processed/telegram_messages_cleaned")

conn = psycopg2.connect(
    host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
)
cur = conn.cursor()

# Create schema and table
cur.execute("""
CREATE SCHEMA IF NOT EXISTS raw;
CREATE TABLE IF NOT EXISTS raw.telegram_messages (
    message_id BIGINT PRIMARY KEY,
    channel_name TEXT,
    date TIMESTAMP,
    message_text TEXT,
    view_count INT,
    forward_count INT,
    has_image BOOLEAN,
    image_path TEXT
)
""")
conn.commit()

# Load JSON files
for json_file in DATA_DIR.rglob("*.json"):
    with open(json_file, "r", encoding="utf-8") as f:
        messages = json.load(f)
        for msg in messages:
            cur.execute("""
                INSERT INTO raw.telegram_messages
                (message_id, channel_name, date, message_text, view_count, forward_count, has_image, image_path)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (message_id) DO NOTHING
            """, (
                msg.get("message_id"),
                msg.get("channel_name"),
                msg.get("date"),
                msg.get("text"),
                msg.get("views"),
                msg.get("forwards"),
                msg.get("has_image", False),
                msg.get("image_path")
            ))
conn.commit()
cur.close()
conn.close()
print("Raw data loaded successfully!")
