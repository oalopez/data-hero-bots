from app.models.execution_info_schema import ExecutionInfo, StatusHistory, AuditData, FileData
import datetime

def start_crawl_execution(bot_name):
    execution = ExecutionInfo(
        execution_id=ObjectId(),
        bot_name=bot_name,
        start_time=datetime.utcnow(),
        status='Started',
        status_history=[StatusHistory(status='Started', timestamp=datetime.utcnow())],
        audit_data=[AuditData(user='system', action='start', timestamp=datetime.utcnow())],
        files=[],
        url_crawled=[]
    )
    execution.save()
    return execution.execution_id