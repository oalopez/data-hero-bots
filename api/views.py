# /api/views.py
'''
This file contains the business logic for the API endpoints.
'''
from fastapi import HTTPException, status
from app.tasks import execute_crawl_task, get_crawl_status, get_crawl_history
from utils.mapping_util import mongo_to_pydantic_exec_info
from app.models.pydantic_execution_info import ExecutionInfo as PydanticExecutionInfo
from config.settings import BOT_NAME, URL_CRAWLED
import logging

logger = logging.getLogger(__name__)

def create_crawl():
    logger.info("Creating new crawl...")
    try:
        # Logic for creating new crawl task
        task = execute_crawl_task.delay()
        response = {
            "execution_id": str(task.id),
            "status": "pending",
            "details": "Crawl task submitted",
            "bot_name": BOT_NAME,
            "url_crawled": URL_CRAWLED
        }
        logger.info(f"Crawl created: {response}")
        return response
    except Exception as e:
        logger.error(f"Error while creating crawl: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while creating crawl")
        # TODO: Routes is already handling this exception. Should we raise it here as well?

def read_crawl_status(execution_id: str):
    # Fetch the status of the crawl task
    execution_status = get_crawl_status(execution_id)
    if not execution_status:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Execution not found")

    # Convert the dictionary to a Pydantic model.
    # The ** operator is used to unpack the dictionary into keyword arguments
    pydantic_execution_status = PydanticExecutionInfo(**execution_status)
    return pydantic_execution_status

def read_crawl_history():
    # Retrieve the entire crawl history
    history = get_crawl_history()
    # Convert the list of dictionaries to a list of Pydantic models
    pydantic_history = [PydanticExecutionInfo(**execution) for execution in history] if history else []
    return pydantic_history