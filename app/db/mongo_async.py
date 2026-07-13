from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings

async_client = AsyncIOMotorClient(settings.MONGO_URI)
async_db = async_client[settings.DATABASE_NAME]


def get_async_collection(collection_name: str = "task_audit_logs"):
    return async_db[collection_name]
    
