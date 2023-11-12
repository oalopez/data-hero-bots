# Project Directory Structure

This README outlines the structure and main components of the project.

## Directory Breakdown

- `api/`
  - `routes.py`: Implementation of the API routes.
  - `views.py`: Logic for handling requests for each endpoint.
  - `errors.py`: Custom error handlers for API responses.

- `app/`
  - `crawler/`
    - `nyt_headlines.py`: Actual crawling execution
  - `models/`
    - `execution_info_schema.py`: Contains the schema for the `execution_info` collection.
  - `rest_client.py`: Client for making external REST calls.
  - `tasks.py`: Celery background tasks definitions.

- `broker/`
  - `celery_config.py`: Configuration for Celery workers and task queues.

- `ci_cd/`
  - `.gitlab-ci.yml`: GitLab CI/CD configuration file.
  - `.github/`
    - `workflows/`
      - `main.yml`: GitHub Actions workflow for CI/CD.

- `config/`
  - `config.json`: Basic configuration for the bot, including the URL to be crawled.
  - `settings.py`: Application settings including DB, broker, and storage config.
  - `logging_config.py`: Configuration for JSON structured logging.

- `envs/`
  - `development/`, `staging/`, `production/`: Environment-specific Docker and configuration files, including `Dockerfile` and `docker-compose.yml` for each environment.

- `logs/`

- `monitoring/`
  - `metrics.py`: Metrics collection for monitoring tools like Prometheus.

- `storage/`
  - `cloud_storage.py`: Abstraction for cloud storage interactions (e.g., AWS S3).

- `tests/`
  - `unit/`: Unit tests for individual modules/functions.
  - `integration/`: Integration tests to test endpoints and integration.

- `utils/`
  - `config_loader.py`: Function to load bot configuration from a JSON file.

- `main.py`: Main module and entry point of the application; loads configuration and starts the API.

- `requirements.txt`: Lists all the Python dependencies for the project.
- `.env`: Environment variables for the application, including the database connection string.
- `.env.example`: Example template of the `.env` file.
- `pytest.ini`: Configuration file for pytest.

- `README.md`: This file.

- `.gitignore`: To avoid committing logs to the repository.
- `.pre-commit-config.yaml`: Pre-commit hook configuration file.

- `Dockerfile`: Base Dockerfile (for development or as a template for others).
- `docker-compose.yml`: Base Docker Compose configuration (for development).

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
