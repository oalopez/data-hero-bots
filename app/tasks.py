# /app/tasks.py
"""
Contains the Celery tasks to be executed asynchronously.
"""
# /app/tasks.py
from celery import Celery, current_task  # Import the Celery instance
from app.crawler.bot import WebCrawler  # Import your specific web crawling class or method
from app.models.execution_info_schema import ExecutionInfo, FileData  # Import your ODM model for MongoDB
from utils.encoders import CustomEncoder  # Import the custom encoder for MongoDB
from datetime import datetime
import json
import config.settings as settings
import logging

logger = logging.getLogger(__name__)

# Configure Celery (make sure to appropriately configure Celery elsewhere, e.g., in a separate config file)
celery_app = Celery('tasks', broker='redis://localhost:6379/0')  # Adjust the broker URL as necessary

@celery_app.task
def execute_crawl_task():
    crawler = WebCrawler(bot_name=settings.BOT_NAME, start_url=settings.URL_CRAWLED)  # Instantiate your crawler class
    execution_data = crawler.start_crawl()  # Start the web crawling process

    logger.info("Execution Data: " + json.dumps(execution_data, cls=CustomEncoder))
    
    execution_info = ExecutionInfo(
        execution_id=current_task.request.id,
        bot_name=execution_data['bot_name'],
        status=execution_data['status'], 
        start_time=execution_data['start_time'],
        end_time=execution_data['end_time'],
        url_crawled=execution_data['url_crawled'],  # Replace with the actual URL that was crawled
        files=[FileData(
            file_type='csv',  # Replace with actual file type
            file_location=execution_data['file_path'],  # Update with appropriate file path
            metadata='Data extracted on {}'.format(datetime.now().isoformat())  # Replace with actual metadata
        )]
    )

    execution_info.save()  # Persist the information to MongoDB
    logger.info("Execution Info Saved: " + json.dumps(execution_info.to_mongo().to_dict(), cls=CustomEncoder))

    # TODO: Should we handle the exception here or in the caller?

    # No need of the return statement since the data is already persisted to MongoDB
    # and we are not calling this task from another task

    #execution_info_dict = execution_info.to_mongo().to_dict()
    #print("Execution Info: " + json.dumps(execution_info_dict, cls=CustomEncoder))

    # Any referenced Objects which are also ObjectIds should be converted likewise
    # Assuming there are no nested ObjectId references in FileData or elsewhere
    #execution_info_dict['_id'] = str(execution_info_dict['_id'])  # Convert ObjectId to string
    #execution_info_dict['execution_id'] = str(execution_info_dict['execution_id'])  # Convert ObjectId to string

    #return execution_info_dict

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