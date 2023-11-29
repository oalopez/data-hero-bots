# Project Directory Structure

This README outlines the structure and main components of the project.

## Directory Breakdown

```
my_bot_module/
│
├── app/                                   # Core logic of the web crawler application
│   ├── crawler/
│   │   └── bot.py                         # Core web crawler logic, responsible for scraping and extracting data from specified URLs.
│   ├── models/                            # Object-Document Mapping (ODM) models for MongoDB
│   │   └── execution_info_schema.py       # Schema for execution_info collection in MongoDB, detailing document structure
│   │   └── pydantic_execution_info.py     # Defines Pydantic models for execution info, ensuring type safety and validation of data before it's processed or stored.
│   ├── rest_client.py                     # Implements a client for making REST API calls to external services
│   └── tasks.py                           # Definitions of Celery background tasks for asynchronous operations
│
├── api/                                   # Handles the REST API interface of the application
│   ├── routes.py                          # Establishes the API routes/endpoints for the application
│   ├── views.py                           # Handles request processing logic for each API endpoint
│   └── errors.py                          # Defines custom error handlers for consistent API error responses
│
├── storage/                               # Modules related to storage operations
│   └── cloud_storage.py                   # Interface for interacting with cloud storage services like AWS S3
│
├── config/                                # Contains configuration files and settings
│   ├── bot_config.json                    # JSON configuration file containing adjustable parameters for the bot.
│   ├── settings.py                        # Central application settings like database, broker, and storage configurations
│   └── logging_config.py                  # Sets up structured logging, potentially in JSON format
│
├── diagrams/
│   └── bot-dataflow.drawio                # A visual representation of the data flow or architecture in the web crawler, editable with draw.io.
│
├── logs/                                  # Directory designated for log file storage
│
├── tests/
│   ├── integration/                       # Contains integration tests to ensure different parts of the application work together seamlessly.
│   └── unit/ 
│       ├── conftest.py                    # Pytest configuration file for setting up fixtures and test environments.
│       └── test_database.py               # Unit tests for database interactions, ensuring data integrity and proper database operations.
│
├── ci_cd/                                 # Holds CI/CD (Continuous Integration & Deployment) configurations
│   ├── .gitlab-ci.yml                     # Configuration file for CI/CD pipelines in GitLab
│   └── .github/                           # Contains GitHub Actions workflows for CI/CD
│       └── workflows/
│           └── main.yml                   # Main GitHub Actions workflow configuration for CI/CD processes
│
├── monitoring/                            # Tools and scripts for monitoring application performance
│   └── metrics.py                         # Collects and defines metrics for monitoring, e.g., with Prometheus
│
├── envs/                                  # Environment-specific configurations and Docker files
│   ├── development/
│   │   ├── Dockerfile                     # Dockerfile for setting up a development environment
│   │   └── docker-compose.yml             # Docker Compose configuration for development setup
│   ├── staging/
│   │   ├── Dockerfile                     # Dockerfile for staging environment setup
│   │   └── docker-compose.yml             # Docker Compose configuration for the staging environment
│   └── production/
│       ├── Dockerfile                     # Dockerfile for production environment setup
│       └── docker-compose.yml             # Docker Compose configuration for production deployment
│
├── utils/
│   ├── config_loader.py                   # Loads and parses the bot configuration from bot_config.json, ensuring the crawler uses the correct settings.
│   ├── encoders.py                        # Custom data encoders, likely for converting complex data types to and from formats like JSON.
│   └── mapping_util.py                    # Utility functions for mapping or transforming data, possibly for normalizing or structuring scraped data.
│
├── .env                                   # Contains environment variables for the project, such as API keys and database URIs.
├── .env.example                           # Template for the .env file, illustrating required environment variables without revealing sensitive information.
├── Dockerfile                             # Base Dockerfile, used for development or as a template for other environments
├── docker-compose.yml                     # Base Docker Compose file for setting up development environment
├── main.py                                # Main entry point for starting the REST API server and Celery Worker
├── pytest.ini                             # Configuration file for pytest, specifying options and settings for running the test suites.
├── requirements.txt                       # Lists required Python packages for the project
├── README.md                              # This file. Project documentation including setup and usage instructions
└── .pre-commit-config.yaml                # Configuration for pre-commit hooks to enforce code standards before commits
```

## Schema Structure for `execution_info`

The `execution_info_schema.py` file defines the following structure:

```json
{
    "execution_id": String,
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
