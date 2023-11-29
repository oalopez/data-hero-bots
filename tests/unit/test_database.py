# tests/unit/test_database.py

import pytest
import mongomock
from mongoengine import connect, disconnect
from app.models.execution_info_schema import ExecutionInfo, StatusHistory, AuditData, FileData
from bson import ObjectId
from datetime import datetime

# Assuming you have added sys.path.append logic to include your app directory

@pytest.fixture(scope='function')
def db_connection():
    # Setup Mock MongoDB connection
    disconnect(alias='default')  # Disconnect from the real MongoDB database
    connect('test_db', host='localhost', alias='default', mongo_client_class=mongomock.MongoClient)  # Connect to the mock MongoDB database

    yield  # this allows to return control to the test after setup

    disconnect(alias='default')  # Disconnect from the mock MongoDB database after the test

def test_execution_info(db_connection):
    
    # Create a new ExecutionInfo object
    execution = ExecutionInfo(
        execution_id='00aa11bb22-1234-abcd-efgh-000000000000',
        bot_name='test_bot',
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow(),
        status='Started',
        status_history=[StatusHistory(status='Started', timestamp=datetime.utcnow())],
        audit_data=[AuditData(user='system', action='start', timestamp=datetime.utcnow())],
        files=[],
        url_crawled=[]
    )
    execution.save()

    # Retrieve the ExecutionInfo object from the database
    execution_from_db = ExecutionInfo.objects(bot_name='test_bot').first()

    # Assert that the object retrieved from the database is the same as the object we created
    assert execution_from_db == execution
    assert execution_from_db.bot_name == 'test_bot'
    assert execution_from_db.status == 'Started'

    execution_from_db = ExecutionInfo.objects(bot_name='non_existent_bot').first()
    assert execution_from_db is None

    pass