from fastapi import APIRouter, Depends, HTTPException

from apps.api_gateway.dependencies import get_trace_repository
from services.data.repositories import TraceRepository
from shared.contracts.traces import TraceResponse

router = APIRouter()


@router.get("/{trace_id}", response_model=TraceResponse)
def get_trace(
    trace_id: str,
    repository: TraceRepository = Depends(get_trace_repository),
) -> TraceResponse:
    trace = repository.get_trace(trace_id)
    if not trace:
        raise HTTPException(status_code=404, detail="Trace not found")
    return TraceResponse(**trace)
