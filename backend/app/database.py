import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "stikerly")
print("USING URI:", MONGO_URI)

client = MongoClient(MONGO_URI, maxPoolSize=1)
db = client[DB_NAME]

try:
    client.admin.command("ping")
    print(f"Connected to MongoDB | DB: {DB_NAME}")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    # We won't raise so the app doesn't crash on init immediately.
    # raise e

templates_collection = db["templates"]
