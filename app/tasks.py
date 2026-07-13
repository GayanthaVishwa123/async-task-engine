import time

from celery import Celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

celery_app = Celery(
    "tasks", broker="redis://redis:6379/0", backend="redis://redis:6379/0"
)

# Advanced Configuration: Routing tasks to distinct queues
celery_app.conf.task_routes = {
    "app.tasks.send_critical_notification": {"queue": "high_priority"},
    "app.tasks.send_bulk_notification": {"queue": "low_priority"},
}


# 1. High Priority Task with Exponential Backoff Retries
@celery_app.task(
    name="send_critical_notification",
    bind=True,
    max_retries=3,
    default_retry_delay=2,  # starts with 2 seconds
    autoretry_for=(RuntimeError,),
    retry_backoff=True,  # Time triples/doubles per retry (2s, 4s, 8s...)
)
def send_critical_notification(self, email: str, message: str):
    logger.info(
        f"Processing critical notification to {email} (Attempt {self.request.retries + 1})"
    )

    # Simulating a third-party API gateway failure for test cases
    if "fail" in email:
        logger.error(f"External notification gateway failed for {email}")
        raise RuntimeError("Gateway Timeout Connecting to Provider")

    time.sleep(1)
    return {"status": "sent", "priority": "high", "to": email}


# 2. Low Priority Task for Bulk Messages
@celery_app.task(name="send_bulk_notification")
def send_bulk_notification(emails: list, message: str):
    logger.info(f"Processing bulk notification for {len(emails)} recipients")
    time.sleep(4)  # Simulating a heavy batch job
    return {"status": "sent", "priority": "low", "count": len(emails)}
