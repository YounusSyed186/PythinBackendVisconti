from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise Exception("MONGO_URI not set in .env")

client = MongoClient(MONGO_URI)
db = client["test"]  # picks DB from URI
