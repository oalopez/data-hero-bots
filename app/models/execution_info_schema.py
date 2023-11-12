from mongoengine import Document, StringField, DateTimeField, ListField, ObjectIdField, EmbeddedDocumentField, EmbeddedDocument, URLField

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
    url_crawled = ListField(StringField())
    screenshot_path = StringField()  # Optional; ensure this is correct as per your actual storage logic

    def __str__(self):
        return f"Execution Info ({self.bot_name}, {self.execution_id})"