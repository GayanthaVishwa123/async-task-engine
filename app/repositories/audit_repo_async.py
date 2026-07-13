from typing import Optional

from app.db.mongo_async import get_async_collection
from app.schemas.audit_schema import TaskAuditLog


class AuditRepoAsync:
    def __init__(self):
        self.collection = get_async_collection()

    async def create_audit(self, audit_in: TaskAuditLog) -> bool:
        doc = audit_in.model_dump()
        result = await self.collection.insert_one(doc)
        return result.acknowledged

    async def get_audit(self, task_id: str) -> Optional[dict]:
        return await self.collection.find_one({"task_id": task_id}, {"_id": 0})
