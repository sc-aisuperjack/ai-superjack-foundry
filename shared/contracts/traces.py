from pydantic import BaseModel


class TraceResponse(BaseModel):
    trace_id: str
    query: str
    provider: str
    route: str
    citations: list[dict]
    answer: str
