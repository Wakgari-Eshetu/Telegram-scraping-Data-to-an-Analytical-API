from ultralytics import YOLO
import os
import pandas as pd


IMAGE_DIR = "data/raw/images"          # Images from Task 1
OUTPUT_CSV = "data/yolo_detections.csv"
MODEL_NAME = "yolov8n.pt"             # YOLOv8 nano for speed


model = YOLO(MODEL_NAME)

results_data = []


for channel_name in os.listdir(IMAGE_DIR):
    channel_path = os.path.join(IMAGE_DIR, channel_name)
    if not os.path.isdir(channel_path):
        continue

    for image_file in os.listdir(channel_path):
        if not image_file.lower().endswith((".jpg", ".png", ".jpeg")):
            continue

        image_path = os.path.join(channel_path, image_file)
        message_id = os.path.splitext(image_file)[0]  # filename without extension

        # Run YOLO detection
        detections = model(image_path)[0]

        has_person = False
        has_product = False
        max_conf = 0.0

        for box in detections.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = model.names[cls_id]

            max_conf = max(max_conf, conf)

            if label == "person":
                has_person = True
            if label in ["bottle", "cup", "container"]:
                has_product = True


        if has_person and has_product:
            category = "promotional"
        elif has_product and not has_person:
            category = "product_display"
        elif has_person and not has_product:
            category = "lifestyle"
        else:
            category = "other"

        results_data.append({
            "message_id": message_id,
            "channel_name": channel_name,
            "image_category": category,
            "confidence_score": round(max_conf, 3)
        })


df = pd.DataFrame(results_data)
df.to_csv(OUTPUT_CSV, index=False)

print(f"YOLO detection completed. CSV saved at {OUTPUT_CSV}")
