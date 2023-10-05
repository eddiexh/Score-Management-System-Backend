# MongoDB.py
from pymongo import MongoClient
import os

def connectDB():
    try:
        client = MongoClient(os.getenv('MongoDB_URI'))
        db = client['SMS']
        return db
    except Exception as e:
        print(e)