from fastapi import APIRouter, Depends

from apps.api_gateway.dependencies import get_document_repository
from services.data.repositories import DocumentRepository
from shared.contracts.documents import DocumentUploadRequest, DocumentUploadResponse
from shared.utils.chunking import chunk_text

router = APIRouter()


@router.post("/upload", response_model=DocumentUploadResponse)
def upload_document(
    payload: DocumentUploadRequest,
    repository: DocumentRepository = Depends(get_document_repository),
) -> DocumentUploadResponse:
    chunks = chunk_text(payload.content, chunk_size=payload.chunk_size, overlap=payload.chunk_overlap)
    document_id = repository.save_document(
        title=payload.title,
        raw_content=payload.content,
        metadata=payload.metadata,
        chunks=chunks,
    )
    return DocumentUploadResponse(document_id=document_id, chunk_count=len(chunks), status="stored")
