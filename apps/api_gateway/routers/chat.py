from fastapi import APIRouter, Depends

from apps.api_gateway.dependencies import get_engine
from services.orchestration.engine import OrchestrationEngine
from shared.contracts.chat import ChatQueryRequest, ChatQueryResponse

router = APIRouter()


@router.post("/query", response_model=ChatQueryResponse)
async def query_chat(
    payload: ChatQueryRequest,
    engine: OrchestrationEngine = Depends(get_engine),
) -> ChatQueryResponse:
    return await engine.run(payload)
