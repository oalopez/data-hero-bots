# /app/views.py
'''
This file contains the business logic for the API endpoints.
'''
from fastapi import HTTPException, status
from app.tasks import execute_crawl_task, get_crawl_status, get_crawl_history

def create_crawl():
    # Logic for creating new crawl task
    task = execute_crawl_task.delay()
    return {"task_id": str(task.id), "status": "pending", "details": "Crawl task submitted"}

def read_crawl_status(execution_id: str):
    # Fetch the status of the crawl task
    execution_status = get_crawl_status(execution_id)
    if not execution_status:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Execution not found")
    return execution_status

def read_crawl_history():
    # Retrieve the entire crawl history
    history = get_crawl_history()
    # No need to raise 404 if history is empty; simply return the empty list
    return list(history) if history else []