from celery import Celery

from shared.config.settings import get_settings

settings = get_settings()
celery_app = Celery("agentic_foundry", broker=settings.redis_url, backend=settings.redis_url)


@celery_app.task
def ingest_document_task(title: str, content: str) -> dict[str, str | int]:
    return {"status": "queued", "title": title, "length": len(content)}
