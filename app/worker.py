from celery import Celery

from app.core.settings import settings

celery_app = Celery(
    "rag_backend",
    broker=settings.celery_broker,
    backend=settings.celery_backend,
    include=["app.modules.document.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)
