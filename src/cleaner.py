import os
import json
import re
import logging
from datetime import datetime


RAW_PATH = "data/raw/telegram_messages"
PROCESSED_PATH = "data/processed/telegram_messages_cleaned"
LOG_PATH = "logs"

os.makedirs(PROCESSED_PATH, exist_ok=True)
os.makedirs(LOG_PATH, exist_ok=True)


logging.basicConfig(
    filename=os.path.join(LOG_PATH, "cleaner.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def clean_text(text):
    if not text:
        return ""

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove emojis & special characters
    text = re.sub(r"[^\w\s.,!?]", "", text)

    # Normalize spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


def clean_file(input_file, output_dir):
    with open(input_file, "r", encoding="utf-8") as f:
        messages = json.load(f)

    cleaned_messages = []

    for msg in messages:
        cleaned_msg = msg.copy()
        cleaned_msg["text"] = clean_text(msg.get("text", ""))
        cleaned_messages.append(cleaned_msg)

    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(
        output_dir, os.path.basename(input_file)
    )

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(cleaned_messages, f, ensure_ascii=False, indent=2)

    logging.info(f"Cleaned: {output_file}")


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    raw_today = os.path.join(RAW_PATH, today)
    processed_today = os.path.join(PROCESSED_PATH, today)

    if not os.path.exists(raw_today):
        logging.warning(f"No raw data for {today}")
        return

    for file in os.listdir(raw_today):
        if file.endswith(".json"):
            clean_file(
                os.path.join(raw_today, file),
                processed_today
            )

    logging.info("Cleaning completed successfully")

if __name__ == "__main__":
    main()
