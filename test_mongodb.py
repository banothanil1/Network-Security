import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_url = os.getenv("MONGO_DB_URL")

try:
    client = MongoClient(mongo_url)

    # Test the connection
    client.admin.command("ping")

    print("MongoDB connection successful!")

except Exception as e:
    print("MongoDB connection failed!")
    print(e)