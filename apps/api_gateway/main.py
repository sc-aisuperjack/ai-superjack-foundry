from fastapi import FastAPI

from apps.api_gateway.routers import chat, documents, speech, traces
from shared.config.settings import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name)
app.include_router(chat.router, prefix="/v1/chat", tags=["chat"])
app.include_router(documents.router, prefix="/v1/documents", tags=["documents"])
app.include_router(speech.router, prefix="/v1/speech", tags=["speech"])
app.include_router(traces.router, prefix="/v1/traces", tags=["traces"])


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name, "env": settings.app_env}
