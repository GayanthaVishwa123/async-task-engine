import logging

from celery.signals import task_failure, task_postrun, task_prerun, task_retry

from app.repositories.audit_repo_sync import AuditRepoSync

logger = logging.getLogger(__name__)
repo = AuditRepoSync()


@task_prerun.connect
def on_task_prerun(task_id, task, args, **kwargs):
    logger.info(f"🚀 Signal: Task {task.name} [{task_id}] is moving to PROCESSING.")
    repo.update_status(task_id=task_id, status="PROCESSING")


@task_postrun.connect
def on_task_postrun(task_id, task, state, retval, **kwargs):
    if state == "SUCCESS":
        logger.info(f"✅ Signal: Task {task.name} [{task_id}] completed successfully.")
        repo.update_status(task_id=task_id, status="SUCCESS", result=str(retval))


@task_retry.connect
def on_task_retry(task_id, exception, sender, **kwargs):
    current_retry = sender.request.retries + 1
    logger.warning(f"🔄 Signal: Task [{task_id}] retrying. Attempt: {current_retry}")
    repo.inc_retry(task_id=task_id, error=str(exception), retries=current_retry)


@task_failure.connect
def on_task_failure(task_id, exception, **kwargs):
    logger.error(f"🚨 Signal: Task [{task_id}] failed permanently.")
    repo.update_status(task_id=task_id, status="FAILURE", error=str(exception))
