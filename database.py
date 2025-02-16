import os
from qdrant_client import QdrantClient
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Debugging: Print environment variables to check if they are loaded
print("🔹 Debugging Environment Variables:")
print(f"MONGO_URI: {os.getenv('MONGO_URI')}")
print(f"QDRANT_HOST: {os.getenv('QDRANT_HOST')}")
print(f"QDRANT_API_KEY: {os.getenv('QDRANT_API_KEY')}")
print(f"GROQ_API_KEY: {os.getenv('GROQ_API_KEY')}")

# 🔹 MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("❌ ERROR: MONGO_URI is not set. Check your .env file.")

mongo_client = MongoClient(MONGO_URI)
db = mongo_client["rag_db"]
documents_collection = db["documents"]

# 🔹 Qdrant Cloud Connection
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

if not QDRANT_HOST or not QDRANT_API_KEY:
    raise ValueError("❌ ERROR: QDRANT_HOST or QDRANT_API_KEY is not set. Check your .env file.")

# Initialize Qdrant Client with Cloud API Key
qdrant_client = QdrantClient(QDRANT_HOST, api_key=QDRANT_API_KEY)
