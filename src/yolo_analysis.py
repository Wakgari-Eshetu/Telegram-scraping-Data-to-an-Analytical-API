import pandas as pd
import json
import os

# Load YOLO CSV
yolo = pd.read_csv("data/yolo_detections.csv")

yolo["message_id"] = yolo["message_id"].astype(str)
# Count images per category
print("Image counts by category:")
print(yolo['image_category'].value_counts())

# Merge with raw messages from Task 1
json_files = []
for root, dirs, files in os.walk("data/raw/telegram_messages"):
    for file in files:
        if file.endswith(".json"):
            json_files.append(os.path.join(root, file))

all_messages = []
for file in json_files:
    with open(file, "r", encoding="utf-8") as f:
        messages = json.load(f)
        for msg in messages:
            all_messages.append({
                "message_id": str(msg.get("message_id") ),
                "text": msg.get("text", ""),
                "views": msg.get("views", 0),
                "channel_name": msg.get("channel_name")
            })

messages_df = pd.DataFrame(all_messages)

# Merge YOLO results with message info
merged = pd.merge(yolo, messages_df, on=["message_id", "channel_name"], how="left")

# Example analysis 1: average views per image category
avg_views = merged.groupby("image_category")["views"].mean()
print("\nAverage views per image category:")
print(avg_views)

# Example analysis 2: number of images per channel
channel_counts = merged.groupby("channel_name")["message_id"].count()
print("\nNumber of images per channel:")
print(channel_counts)
