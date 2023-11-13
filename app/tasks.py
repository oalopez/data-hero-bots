# /app/tasks.py
"""
Contains the Celery tasks to be executed asynchronously.
"""
# /app/tasks.py
from celery import Celery
from app.crawler.bot import WebCrawler  # Import your specific web crawling class or method
from app.models.execution_info_schema import ExecutionInfo  # Import your ODM model for MongoDB

# Configure Celery (make sure to appropriately configure Celery elsewhere, e.g., in a separate config file)
celery_app = Celery('tasks', broker='redis://localhost:6379/0')  # Adjust the broker URL as necessary

@celery_app.task
def execute_crawl_task():
    crawler = WebCrawler()  # Instantiate your crawler class
    execution_data = crawler.start_crawl()  # Start the web crawling process

    # Save completion info to MongoDB
    execution_info = ExecutionInfo(
        execution_id=execute_crawl_task.request.id,  # Retrieve task id from Celery
        status='completed',
        start_time=execution_data['start_time'],
        end_time=execution_data['end_time'],
        data_file_path=execution_data['file_path']  # Update with appropriate file path or reference
    )
    execution_info.save()  # Persist the information to MongoDB

    return execution_info.to_mongo().to_dict()

def get_crawl_status(execution_id):
    try:
        # Retrieve the execution information from MongoDB using the execution_id
        execution_info = ExecutionInfo.objects.get(execution_id=execution_id)
    
        # Convert the execution_info document to a Python dictionary or a JSON response
        return execution_info.to_mongo().to_dict()
    except ExecutionInfo.DoesNotExist:
        return None  # Return None if not found

def get_crawl_history():
    # Retrieve all the documents from MongoDB
    history = ExecutionInfo.objects.all()
    
    # Convert the queryset to a list of Python dictionaries
    return [execution.to_mongo().to_dict() for execution in history]