from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class TaskAuditLog(BaseModel):
    task_id: str = Field(..., description="The unique Celery task instance ID")
    task_name: str
    queue: str
    status: str = "PENDING"  # PENDING -> PROCESSING -> SUCCESS / RETRY / FAILURE
    args: Optional[list] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    retries: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
