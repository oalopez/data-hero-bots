# main.py
"""
Main module. This is the entry point of the application.
Loads the configuration, starts the API and the Celery worker, and connects to the database.    
"""
import config.settings as settings

# Initialize Celery
from celery import Celery
celery_app = Celery(settings.BOT_NAME + '_module')
celery_app.config_from_object('config.settings')

# Connect to MongoDB
from mongoengine import connect
connect(
    db=settings.MONGO_DB_NAME,
    host=settings.MONGO_HOST,
    port=settings.MONGO_PORT
)

# Initialize FastAPI
from fastapi import FastAPI
from api.routes import router as api_router
app = FastAPI()
app.include_router(api_router)

# Run the API with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# TODO: port should be configurable
# TODO: run uvicorn programmatically is not recommended for production