import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

from app.repositories.audit_repo_async import AuditRepoAsync
from app.schemas.audit_schema import TaskAuditLog
from app.tasks import send_bulk_notification, send_critical_notification

app = FastAPI(title="Production Engine with Lifecycle Audit Trail")
audit_repo = AuditRepoAsync()


class CriticalSchema(BaseModel):
    email: EmailStr
    message: str


@app.post("/notify/critical")
async def trigger_critical_notification(payload: CriticalSchema):
    # 1. Generate Custom Task ID ahead of time
    custom_task_id = str(uuid.uuid4())

    # 2. Write the PENDING log to Mongo using Async driver
    audit_log = TaskAuditLog(
        task_id=custom_task_id,
        task_name="app.tasks.send_critical_notification",
        queue="high_priority",
        args=[payload.email, payload.message],
    )
    await audit_repo.create_audit(audit_log)

    # 3. Fire the Celery task with the predefined ID
    send_critical_notification.apply_async(
        args=[payload.email, payload.message], task_id=custom_task_id
    )

    return {"status": "Dispatched to Queue", "task_id": custom_task_id}


@app.get("/tasks/audit/{task_id}")
async def get_task_lifecycle_log(task_id: str):
    log = await audit_repo.get_audit(task_id)
    if not log:
        raise HTTPException(
            status_code=404, detail="Requested task log audit trail not found"
        )
    return log
