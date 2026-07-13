import time

from celery import Celery

from app.config import settings

celery_app = Celery("tasks", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

# Enforce Celery to discover signal receivers
import app.celery_signals

celery_app.conf.task_routes = {
    "app.tasks.send_critical_notification": {"queue": "high_priority"},
    "app.tasks.send_bulk_notification": {"queue": "low_priority"},
}


@celery_app.task(
    name="app.tasks.send_critical_notification",
    bind=True,
    max_retries=2,
    default_retry_delay=4,
)
def send_critical_notification(self, email: str, message: str):
    # 'fail' කියන වචනය ඊමේල් එකේ තිබ්බොත් සිග්නල් සහ රිට්‍රයි ටෙස්ට් කරන්න auto fail කරනවා
    if "fail" in email.lower():
        raise RuntimeError("External SMS/Email Gateway Timeout Connection Exception")

    time.sleep(1)
    return {"delivered": True, "channel": "SMS"}


@celery_app.task(name="app.tasks.send_bulk_notification")
def send_bulk_notification(emails: list[str], message: str):
    time.sleep(2)
    return {"batch_size": len(emails), "status": "sent"}
