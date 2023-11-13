# main.py
"""
Main module. This is the entry point of the application.
Loads the configuration, starts the API and the Celery worker, and connects to the database.
"""
import config.settings
from fastapi import FastAPI
from api.routes import router as api_router
from celery import Celery
from mongoengine import connect

connect(
    db=config.settings.MONGO_DB_NAME,
    host=config.settings.MONGO_HOST,
    port=config.settings.MONGO_PORT,
    username=config.settings.MONGO_USERNAME,
    password=config.settings.MONGO_PASSWORD
)


# Initialize Celery
celery_app = Celery('my_bot_module')
celery_app.config_from_object('config.celery_config')

# Initialize FastAPI
app = FastAPI()
app.include_router(api_router)

# Run the API with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# TODO: port should be configurable
# TODO: run uvicorn programmatically is not recommended for production