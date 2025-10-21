from pymongo import MongoClient


# init database
client = MongoClient("localhost", port=27017)
role_db = client["role_db"]

# init collections
users = role_db["users"]
levels = role_db["levels"]
shop_items = role_db["shop_items"]
baseTasks = role_db["baseTasks"]
tasks = role_db["tasks"]
