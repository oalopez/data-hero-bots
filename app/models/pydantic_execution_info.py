# models/pydantic_execution_info.py

from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from enum import Enum
from bson import ObjectId

# You can create Pydantic-compatible types for object id
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, v):
        return {"type": "string"}

# Define Enums for the status choices
# TODO: Enums should be defined in a separate file
class CrawlStatus(str, Enum):
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETED = 'completed'
    FAILED = 'failed'

class StatusHistory(BaseModel):
    status: CrawlStatus
    timestamp: datetime

class AuditData(BaseModel):
    user: str
    action: str
    timestamp: datetime

class FileData(BaseModel):
    file_type: str
    file_location: str
    metadata: Optional[str] = None

class ExecutionInfo(BaseModel):
    execution_id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    bot_name: str
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    status: CrawlStatus
    status_history: List[StatusHistory] = []
    audit_data: List[AuditData] = []
    files: List[FileData] = []
    url_crawled: HttpUrl
    screenshot_path: Optional[str] = None

    class Config:
        populate_by_name = True  # Allows using MongoDB's _id as field name
        json_encoders = {
            ObjectId: str  # JSON representation for ObjectId
        }
        json_schema_extra = {
            "example": {
                "bot_name": "sample_bot",
                "status": "pending",
                "status_history": [
                    {
                        "status": "pending",
                        "timestamp": "2023-04-01T12:00:00Z"
                    }
                ],
                "audit_data": [
                    {
                        "user": "admin_user",
                        "action": "Started crawl task",
                        "timestamp": "2023-04-01T12:00:00Z"
                    }
                ],
                "files": [
                    {
                        "file_type": "csv",
                        "file_location": "/path/to/data.csv",
                        "metadata": "Data extracted on 2023-04-01"
                    }
                ],
                "url_crawled": "http://example.com/page",
                "screenshot_path": "/path/to/screenshot.png"
            }
        }