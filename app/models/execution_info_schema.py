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
from config import settings

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
    meta = {'collection': 'execution_info'}
    
    execution_id = ObjectIdField(required=True, primary_key=True)
    bot_name = StringField(required=True)
    start_time = DateTimeField(required=True)
    end_time = DateTimeField(required=True)
    status = StringField(required=True)
    status_history = ListField(EmbeddedDocumentField(StatusHistory))
    audit_data = ListField(EmbeddedDocumentField(AuditData))
    files = ListField(EmbeddedDocumentField(FileData))
    url_crawled = StringField()
    screenshot_path = StringField()

    def __str__(self):
        return f"Execution Info ({self.bot_name}, {self.execution_id})"
    
    @classmethod
    def start_execution(cls, bot_name):
        execution = cls(
            execution_id=ObjectId(),
            bot_name=bot_name,
            start_time=datetime.utcnow(),
            status='Started',
            status_history=[StatusHistory(status='Started', timestamp=datetime.utcnow())],
            audit_data=[AuditData(user='system', action='start', timestamp=datetime.utcnow())],
            files=[],
            url_crawled=settings.URL_CRAWLED
        )
        execution.save()
        return execution.execution_id
    
    # ExecutionInfo.save_headlines_to_csv(headlines, execution_id)  # Implement this function in the ODM
    @classmethod
    def save_headlines_to_csv(cls, headlines, execution_id):
        # Save the headlines to a CSV file and return the file path
        
        # TODO: Implement this function. Should this logic be in the ODM?
        file_path = f"/tmp/{execution_id}.csv"

        return file_path
    
    # finish_execution(execution_id, file_path, urls_crawled)
    @classmethod
    def finish_execution(cls, execution_id, file_path):
        execution = cls.objects(execution_id=execution_id).first()
        execution.end_time = datetime.utcnow()
        execution.status = 'Finished'
        execution.status_history.append(StatusHistory(status='Finished', timestamp=datetime.utcnow()))
        execution.audit_data.append(AuditData(user='system', action='finish', timestamp=datetime.utcnow()))
        execution.files.append(FileData(file_type='csv', file_location=file_path))
        execution.url_crawled = settings.URL_CRAWLED
        execution.save()
    
# TODO: status should be an enum