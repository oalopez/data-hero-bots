# Project Directory Structure

This README outlines the structure and main components of the project.

## Directory Breakdown

- `api/`
  - `routes.py`: Implementation of the API routes.
- `app/`
  - `crawler/`
    - `nyt_headlines.py`: Actual crawling execution
  - `models/`
    - `execution_info_schema.py`: Contains the schema for the `execution_info` collection. (Details of the schema structure are included in the file.)
  - `rest_client.py`: Module containing the REST client for API calls.
  - `tasks.py`: Contains the Celery tasks for asynchronous execution.
- `broker/`: 
- `ci_cd/`: 
- `config/`
  - `config.json`: Basic configuration for the bot, including the URL to be crawled.
  - `settings.py`: Settings for the application, including database and URL configurations.
- `envs/`: 
- `logs/`: 
- `monitoring/`: 
- `tests/`
  - `integration/`: 
  - `unit/`
    - `conftest.py`: 
    - `test_database.py`: 
- `utils/`
  - `config_loader.py`: Function to load bot configuration from a JSON file.
- `.env`: Environment variables for the application, including the database connection string.
- `.env.example`: Example template of the `.env` file.
- `main.py`: Main module and entry point of the application; loads configuration and starts the API.
- `pytest.ini`: Configuration file for pytest.
- `README.md`: This file.
- `requirements.txt`: Lists all the Python dependencies for the project.

## Schema Structure for `execution_info`

The `execution_info_schema.py` file defines the following structure:

```json
{
    "execution_id": ObjectId,
    "bot_name": String,
    "start_time": DateTime,
    "end_time": DateTime,
    "status": String,
    "status_history": [
        {
            "status": String,
            "timestamp": DateTime
        }
    ],
    "audit_data": [
        {
            "user": String,
            "action": String,
            "timestamp": DateTime
        }
    ],
    "files": [
        {
            "file_type": String,
            "file_location": String,
            "metadata": String
        }
    ],
    "url_crawled": String,
    "screenshot_path": String
}
