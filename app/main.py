from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

from app.tasks import send_bulk_notification, send_critical_notification

app = FastAPI(title="Advanced Async Task Engine")


class CriticalNotificationSchema(BaseModel):
    email: EmailStr
    message: str


class BulkNotificationSchema(BaseModel):
    emails: List[EmailStr]
    message: str


@app.get("/")
def health_check():
    return {"status": "healthy", "environment": "production-ready"}


@app.post("/notify/critical")
def trigger_critical_notification(payload: CriticalNotificationSchema):
    # Triggers high_priority queue routing
    task = send_critical_notification.delay(payload.email, payload.message)
    return {"status": "Queued in high_priority", "task_id": task.id}


@app.post("/notify/bulk")
def trigger_bulk_notification(payload: BulkNotificationSchema):
    # Triggers low_priority queue routing
    task = send_bulk_notification.delay(payload.emails, payload.message)
    return {"status": "Queued in low_priority", "task_id": task.id}
