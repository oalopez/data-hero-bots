# main.py
"""
Main module. This is the entry point of the application.
Loads the configuration and starts the API.
"""

from fastapi import FastAPI
from api.routes import router as api_router

app = FastAPI()

app.include_router(api_router)