from pymongo import MongoClient
from models.settings import settings

import logging

# init database
client = MongoClient(settings.mongo_address, port=27017)
role_db = client["role_db"]

# init collections
users = role_db["users"]
levels = role_db["levels"]
shop_items = role_db["shop_items"]
baseTasks = role_db["baseTasks"]
tasks = role_db["tasks"]

logging.warning(f"Database: {client.list_database_names()}")  # или client.list_database_names()
logging.warning(f"Collections in role_db: {role_db.list_collection_names()}")
