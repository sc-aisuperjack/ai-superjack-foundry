from dataclasses import dataclass

from services.data.repositories import DocumentRepository


@dataclass
class RetrievalService:
    repository: DocumentRepository

    def retrieve(self, query: str, limit: int = 3) -> dict:
        results = self.repository.search_chunks(query=query, limit=limit)
        return {"query": query, "results": results}
