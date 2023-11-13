# /config/settings.py
"""
This module contains the settings for the application.
Includes the configuration for the database and the URL to be crawled.
"""
import os

# Load environment variables from .env file if present
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'bot_data')  # Default value if not set
MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')  # Default value if not set
MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))  # Default value if not set
MONGO_USERNAME = os.getenv('MONGO_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')

from utils.config_loader import load_config
# Path to JSON config file
CONFIG_PATH = "./config.json"
# Load the configuration
config = load_config(CONFIG_PATH)
# Access the URL configuration from the loaded configuration dictionary
URL_CRAWLED = config.get("url_crawled", "http://example.com/")