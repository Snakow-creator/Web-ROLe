from pymongo import MongoClient

client = MongoClient("localhost", port=27017)
role_db = client["role_db"]
