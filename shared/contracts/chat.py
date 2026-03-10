from pydantic import BaseModel, Field


class ChatQueryRequest(BaseModel):
    query: str = Field(min_length=1)
    provider: str = "mock"
    mode: str = "text"
    conversation_id: str | None = None


class Citation(BaseModel):
    document_id: str
    title: str
    excerpt: str


class ChatQueryResponse(BaseModel):
    answer: str
    citations: list[Citation]
    trace_id: str
    provider: str
    route: str


class SpeechSynthesisRequest(BaseModel):
    text: str = Field(min_length=1)
