from pymongo import MongoClient

from app.config import settings

sync_client = MongoClient(settings.MONGO_URI)
sync_db = sync_client[settings.DATABASE_NAME]


def get_sync_collection(collection_name: str = "task_audit_logs"):
    return sync_db[collection_name]
