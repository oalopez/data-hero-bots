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
```

## Architecture Components:

1. **Crawling Bots (Microservices):**
   Each bot is an independent microservice written in Python, designed to crawl and extract data from a specific source on the internet. They encapsulate the entire data extraction logic and are capable of running as stand-alone services that interact with other system components via REST API calls.

2. **Bot Engine:**
   This is a centralized coordinator or controller that schedules and dispatches crawl tasks to the appropriate bot microservices. It can queue tasks, monitor progress, and handle retries or failures. The Bot Engine might also handle the distribution of work amongst the bot instances and coordinate their scaling.

3. **Redis & Celery:**
   Redis serves as a message broker and a fast, in-memory data store for Celery, which is used for managing background tasks and asynchronous workflows. Celery workers consume tasks from Redis queues, allowing for distributed task processing. This setup enables bots to perform long-duration, resource-intensive crawls without blocking the main execution flow.

4. **MongoDB:**
   This is the primary data storage solution for the microservices, where execution data and extracted content are stored. It allows bots to save data in a flexible, schema-less format, and is suitable for handling large volumes of data. MongoDB is used to persist execution details such as start and end times, statuses, historical execution metadata, and paths to the files that contain the extracted data.

5. **Service Aggregator with WebSocket (FastAPI):**
   The Service Aggregator is a central microservice that aggregates data from the various bots and serves it to the React App. It exposes REST API endpoints for bots to notify it about status updates, which it then broadcasts to the React App through WebSocket connections. It also provides WebSocket endpoints that facilitate a persistent, full-duplex communication channel between the server and the React App  for real-time updates.

6. **API Gateway:**
   This acts as the front door for all requests from clients (including the React App), routing them to the appropriate microservices (including the Service Aggregator and the bot microservices). It abstracts the internal structure of the microservices network and provides security measures like rate limiting and IP filtering.

7. **Authentication Service:**
   Although not directly involved with the bots, the Authentication Service is responsible for managing user authentication and authorization. It would verify user credentials and issue tokens (e.g., JWT) to secure communication between the clients and the microservices using OAuth, OpenID Connect, or similar protocols.

8. **React App:**
   This is the user interface, developed with React, which communicates with the back-end microservices through the API Gateway and WebSocket connections. The App has a Dashboard to display the status of all bots, provides interfaces for starting or stopping crawl tasks, allows viewing of historical data, and downloads files.

## Data Flow for the Reacts App's Dashboard:

1. **Initialization and Bot List Retrieval:**
   When a user first accesses the Dashboard, the React App sends a request through the API Gateway to fetch a list of all bots from the Service Aggregator.

2. **Establishing WebSocket Connection:**
   The React app then establishes a WebSocket connection with the Service Aggregator's endpoint designed specifically for real-time communication.

3. **Crawling Bot Activities and Notifications:**
   As bots perform their crawling activities, any change in their state (if a job starts, fails, succeeds, etc.) results in an immediate REST API call from the bot to the Service Aggregator, including details of the updated execution status.

4. **Broadcasting Real-Time Status:**
   The Service Aggregator receives status updates and transmits them to the React App via the established WebSocket connection. The React App's Dashboard is updated in real-time to reflect these changes.

5. **React App's Display and Interaction:**
   The React App displays the most recent information about each bot's status. Users can directly control bots via the UI, sending commands back via REST API.

6. **Execution History and Data Downloads:**
   When historical execution data is needed, the React App queries the Service Aggregator through the API Gateway. The Service Aggregator retrieves this data from MongoDB and supplies the requested data to the Dashboard, which updates the UI accordingly. 
