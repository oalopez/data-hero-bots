from mongoengine import connect
from config.settings import MONGO_DB_NAME, MONGO_HOST, MONGO_PORT, MONGO_USERNAME, MONGO_PASSWORD

connect(
    db=MONGO_DB_NAME,
    host=MONGO_HOST,
    port=MONGO_PORT,
    username=MONGO_USERNAME,
    password=MONGO_PASSWORD
)