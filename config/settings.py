# /config/settings.py
"""
This module contains the settings for the application.
Includes the configuration for the database and the URL to be crawled.
"""
import os


# TODO: Use pydantic BaseSettings for configuration instead of dotenv

# Load environment variables from .env file if present
from dotenv import load_dotenv
load_dotenv()

# Database configuration
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'bot_data')  # Default value if not set
MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')  # Default value if not set
MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))  # Default value if not set
MONGO_USERNAME = os.getenv('MONGO_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')

# Bot configuration
from utils.config_loader import load_config
BOT_CONFIG_FILE_PATH = "./config/bot_config.json"
bot_config = load_config(BOT_CONFIG_FILE_PATH)
URL_CRAWLED = bot_config.get("url_crawled", "http://example.com/")
BOT_NAME = bot_config.get("bot_name", "empty_bot_name")

# Celery configuration
broker_url = 'redis://localhost:6379/0'  # Default Redis broker URL
result_backend = 'redis://localhost:6379/0'  # Default Redis backend URL
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'
enable_utc = True

#TODO: configure in .env file (or other config source)