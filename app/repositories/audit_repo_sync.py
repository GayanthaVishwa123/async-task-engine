from datetime import datetime

from app.db.mongo_sync import get_sync_collection


class AuditRepoSync:
    def __init__(self):
        self.collection = get_sync_collection()

    def update_status(
        self, task_id: str, status: str, result: str = None, error: str = None
    ):
        update_data = {"status": status, "updated_at": datetime.utcnow()}
        if result is not None:
            update_data["result"] = result
        if error is not None:
            update_data["error"] = error

        self.collection.update_one({"task_id": task_id}, {"$set": update_data})

    def inc_retry(self, task_id: str, error: str, retries: int):
        self.collection.update_one(
            {"task_id": task_id},
            {
                "$set": {
                    "status": "RETRY",
                    "error": error,
                    "retries": retries,
                    "updated_at": datetime.utcnow(),
                }
            },
        )
