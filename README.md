# Medical Telegram Data Warehouse

## Description
This project is a **Telegram data scraping and processing pipeline** focused on Ethiopian medical business channels.  

It extracts messages and images from public Telegram channels, cleans and preprocesses the text, and organizes the data in a structured **data lake**.  

The project also includes a **dbt warehouse** for transformations and a **FastAPI** interface for future analytics.  

---

## Features

- Scrape Telegram messages and images from multiple channels
- Store raw data in a partitioned **data lake**
- Clean and preprocess text while keeping metadata
- Organize images and messages by channel
- Logging for all scraping and cleaning operations
- CI/CD workflow for unit tests and linting
- Prepared for dbt modeling and analytics

---

## Project Structure

