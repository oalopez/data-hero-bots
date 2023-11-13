# /app/models/execution_info_schema.py
"""
This module contains the schema for the execution_info collection.
The structure of the collection is as follows:
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
"""

from mongoengine import Document, StringField, DateTimeField, ListField, ObjectIdField, EmbeddedDocumentField, EmbeddedDocument, URLField
from bson import ObjectId
from datetime import datetime
class StatusHistory(EmbeddedDocument):
    status = StringField(required=True)
    timestamp = DateTimeField(required=True)

class AuditData(EmbeddedDocument):
    user = StringField(required=True)
    action = StringField(required=True)
    timestamp = DateTimeField(required=True)

class FileData(EmbeddedDocument):
    file_type = StringField(required=True)
    file_location = StringField(required=True)
    metadata = StringField()

class ExecutionInfo(Document):
    """
    Schema representing the execution details of a crawl task.
    """
    execution_id = ObjectIdField(default=lambda: ObjectId())  # If you want to use custom execution_id
    bot_name = StringField(required=True)
    start_time = DateTimeField(default=datetime.utcnow)
    end_time = DateTimeField()
    status = StringField(required=True, choices=('pending', 'running', 'completed', 'failed'))
    status_history = ListField(EmbeddedDocumentField(StatusHistory))
    audit_data = ListField(EmbeddedDocumentField(AuditData))
    files = ListField(EmbeddedDocumentField(FileData))
    url_crawled = URLField(required=True)
    screenshot_path = StringField()  # Assuming this is the filesystem path or URL to the screenshot

    meta = {
        'collection': 'execution_info',
        'indexes': [
            'bot_name',
            'status',
            '-start_time',
            # You may add other indexes based on the query patterns of your application.
        ],
        'ordering': ['-start_time']
    }
    
# TODO: status should be an enum