import json
import pytest
from pathlib import Path
from src.cleaner import clean_text, clean_file


def test_clean_text_urls_emojis():
    raw_text = "Buy now! Visit https://t.me/test"
    cleaned = clean_text(raw_text)
    assert cleaned == "Buy now! Visit"

def test_clean_text_empty():
    assert clean_text("") == ""
    assert clean_text(None) == ""

def test_clean_text_special_chars():
    raw_text = "Hello!!! ### @@"
    cleaned = clean_text(raw_text)
    assert cleaned == "Hello!!!"


def test_clean_file(tmp_path):
    # Create fake raw JSON file
    fake_messages = [
        {"text": "Hello http://link.com", "message_id": 1, "date": "2026-01-18", "views": 10, "forwards": 0, "media": None, "image_path": None},
        {"text": "New Product", "message_id": 2, "date": "2026-01-18", "views": 5, "forwards": 1, "media": None, "image_path": None}
    ]

    input_file = tmp_path / "channel.json"
    with open(input_file, "w", encoding="utf-8") as f:
        json.dump(fake_messages, f)

    # Output directory
    output_dir = tmp_path / "cleaned"
    clean_file(str(input_file), str(output_dir))

    output_file = output_dir / "channel.json"
    assert output_file.exists()

    # Load cleaned data
    with open(output_file, "r", encoding="utf-8") as f:
        cleaned_messages = json.load(f)

    # Test that text is cleaned
    assert cleaned_messages[0]["text"] == "Hello"
    assert cleaned_messages[0]["message_id"] == 1
    assert cleaned_messages[1]["text"] == "New Product"
    assert cleaned_messages[1]["message_id"] == 2


def test_dummy():
    assert 1 + 1 == 2
