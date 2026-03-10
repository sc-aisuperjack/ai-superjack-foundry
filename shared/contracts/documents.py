from pydantic import BaseModel, Field


class DocumentUploadRequest(BaseModel):
    title: str = Field(min_length=1)
    content: str = Field(min_length=1)
    metadata: dict = {}
    chunk_size: int = 500
    chunk_overlap: int = 50


class DocumentUploadResponse(BaseModel):
    document_id: str
    chunk_count: int
    status: str
