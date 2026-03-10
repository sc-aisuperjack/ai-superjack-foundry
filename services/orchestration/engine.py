import uuid
from dataclasses import dataclass

from services.memory.cache import RedisCache
from services.data.repositories import TraceRepository
from services.llm_router.factory import get_llm_provider
from services.retrieval.service import RetrievalService
from shared.config.settings import Settings
from shared.contracts.chat import ChatQueryRequest, ChatQueryResponse, Citation


@dataclass
class OrchestrationEngine:
    retrieval_service: RetrievalService
    cache: RedisCache
    trace_repository: TraceRepository
    settings: Settings

    async def run(self, payload: ChatQueryRequest) -> ChatQueryResponse:
        trace_id = str(uuid.uuid4())
        normalized_provider = (payload.provider or self.settings.default_llm_provider).strip().lower()
        cache_key = f"chat:{normalized_provider}:{payload.query.strip().lower()}"
        cached = self.cache.get_json(cache_key)
        if cached:
            return ChatQueryResponse(**cached)

        retrieval_result = self.retrieval_service.retrieve(payload.query)
        llm_provider = get_llm_provider(normalized_provider, self.settings)
        answer = await llm_provider.answer(
            query=payload.query,
            context_chunks=[item["content"] for item in retrieval_result["results"]],
        )
        citations = [
            Citation(document_id=item["document_id"], title=item["title"], excerpt=item["content"][:180])
            for item in retrieval_result["results"]
        ]
        response = ChatQueryResponse(
            answer=answer,
            citations=citations,
            trace_id=trace_id,
            provider=normalized_provider,
            route="retrieve_then_answer",
        )
        self.trace_repository.save_trace(
            {
                "trace_id": trace_id,
                "query": payload.query,
                "provider": normalized_provider,
                "route": "retrieve_then_answer",
                "citations": [citation.model_dump() for citation in citations],
                "answer": answer,
            }
        )
        self.cache.set_json(cache_key, response.model_dump(), ttl_seconds=300)
        return response
