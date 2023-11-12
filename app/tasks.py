# /app/tasks.py
"""
Contains the Celery tasks to be executed asynchronously.
"""
from celery import Celery
from app.crawler import fetch_nyt_headlines
from app.models import ExecutionInfo  # Adjust to actual import

# Assuming 'redis://localhost:6379/0' is our broker URL
celery_app = Celery('crawler', broker='redis://localhost:6379/0')

@celery_app.task
def execute_crawl_task():
    """
    This task starts the NYT headline crawling process.
    It is assumed that fetch_nyt_headlines function exists in the crawler module,
    performing the crawling and returning a list of headlines.
    """
    execution_id = ExecutionInfo.start_execution()  # Starts execution and returns an ID; implement this function in the ODM
    headlines = fetch_nyt_headlines()  # Perform the crawl; implement this and handle results properly

    # Save the fetched headlines into a CSV file and retrieve the file path
    file_path = ExecutionInfo.save_headlines_to_csv(headlines, execution_id)  # Implement this function in the ODM
    
    # Update the execution info with the crawl results
    ExecutionInfo.finish_execution(execution_id, file_path)  # Implement this function in the ODM
    
    # Return execution details at the end of the task
    return ExecutionInfo.get_by_id(execution_id)  # Replace get_by_id with your method in the ODM to fetch execution data

@celery_app.task
def get_crawl_status(execution_id):
    """
    This task fetches the status of a specific crawl task.
    The task is meant to return relevant information about a crawl task's execution.
    """
    return ExecutionInfo.get_by_id(execution_id)  # Replace get_by_id with your ODM method to fetch execution data

@celery_app.task
def get_crawl_history():
    """
    This task retrieves a history of previous crawl executions.
    It should return a list of execution info data for each historical execution.
    """
    return list(ExecutionInfo.get_all())  # Replace get_all with your ODM method to fetch all execution data