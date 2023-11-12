# tests/conftest.py
from dotenv import load_dotenv
load_dotenv()


import pytest
from mongoengine import connect, disconnect
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from config import settings

@pytest.fixture(scope='function')
def mongo_db():
    # If the testing database doesn't have auth enabled, omit username and password
    connect(
        db=settings.MONGO_DB_NAME,
        host=settings.MONGO_HOST,
        port=settings.MONGO_PORT,
    )
    yield
    disconnect()