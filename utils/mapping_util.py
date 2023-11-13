# /utils/mapping_util.py

from app.models.execution_info_schema import ExecutionInfo as MongoExecutionInfo
from app.models.pydantic_execution_info import ExecutionInfo as PydanticExecutionInfo

def mongo_to_pydantic_exec_info(mongo_exec_info: MongoExecutionInfo) -> PydanticExecutionInfo:
    return PydanticExecutionInfo(
        execution_id=mongo_exec_info.execution_id,
        bot_name=mongo_exec_info.bot_name,
        start_time=mongo_exec_info.start_time,
        end_time=mongo_exec_info.end_time,
        status=mongo_exec_info.status,
        status_history=mongo_exec_info.status_history,
        audit_data=mongo_exec_info.audit_data,
        files=mongo_exec_info.files,
        url_crawled=mongo_exec_info.url_crawled,
        screenshot_path=mongo_exec_info.screenshot_path,
    )