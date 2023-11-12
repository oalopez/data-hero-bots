# /api/routes.py
"""
Implementation of the API routes.
"""
from fastapi import APIRouter, HTTPException, Path, status
from app.tasks import execute_crawl_task, get_crawl_status, get_crawl_history
from app.models.execution_info_schema import ExecutionInfo  # Replace with the correct path and model

router = APIRouter()

@router.post("/crawls", response_model=ExecutionInfo, status_code=status.HTTP_201_CREATED)
def create_crawl():
    """Starts a new crawl task and returns the execution info."""
    # The task should be an asynchronous background task; using 'delay()' to enqueue the task
    task = execute_crawl_task.delay()
    return {"task_id": str(task.id), "status": "pending", "details": "Crawl task submitted"}  # Adjust based on your model

@router.get("/crawls/{execution_id}", response_model=ExecutionInfo)
def read_crawl_status(execution_id: str = Path(..., title="The ID of the crawl execution")):
    """Retrieves the status and details of a specific crawl task."""
    # Fetch the status of the crawl task; ensuring consistency between async task ID and MongoDB execution ID
    execution_status = get_crawl_status(execution_id)
    if not execution_status:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Execution not found")
    return execution_status.get()

@router.get("/crawls", response_model=list[ExecutionInfo])
def read_crawl_history():
    """Fetches historical data of crawl executions."""
    # Retrieve the entire crawl history from the MongoDB collection
    history = get_crawl_history()
    if history is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No crawl history available")
    return list(history)
