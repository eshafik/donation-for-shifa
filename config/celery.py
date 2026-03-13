# config/celery.py
# Celery 5.6+; Python 3.14 compatible. Use celery[redis] and redis>=5.0.
from celery import Celery

from config.settings import (
    CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND,
    INSTALLED_APPS,
)

celery_app = Celery(
    "donation-for-shifa",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    result_expires=3600,
    worker_prefetch_multiplier=1,  # fairness: one task at a time per worker
)

# Auto-discover tasks from INSTALLED_APPS (e.g. apps.user.tasks)
celery_app.autodiscover_tasks(INSTALLED_APPS)

# Note: Tasks are sync by default. If a task needs Tortoise ORM, run
# asyncio.run(init_db()) and then asyncio.run(your_async_work()) inside the task body.
