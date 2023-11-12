# /utils/config_loader.py
"""
This module contains the function to load the bot configuration from a JSON file.
"""
import json
from typing import Any, Dict

def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load the configuration from a JSON file.

    :param config_path: Path to the JSON config file.
    :return: A dictionary with the configuration.
    """
    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        print(f"Configuration file not found at {config_path}.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error decoding JSON configuration file at {config_path}.")
        exit(1)
    except Exception as e:
        print(f"An error occurred while loading the configuration: {e}")
        exit(1)