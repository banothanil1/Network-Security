import pymongo
import certifi
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

print("Python MongoDB test started")

client = pymongo.MongoClient(
    MONGO_DB_URL,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=10000
)

print("Client created")

print(client.admin.command("ping"))

print("MongoDB connection successful!")