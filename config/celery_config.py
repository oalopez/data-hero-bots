 # broker/celery_config.py
   
# Celery configuration file
broker_url = 'redis://localhost:6379/0'  # Default Redis broker URL
result_backend = 'redis://localhost:6379/0'  # Default Redis backend URL
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'
enable_utc = True

#TODO: configure in .env file (or other config source)