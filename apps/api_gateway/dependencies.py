from services.memory.cache import RedisCache
from services.data.repositories import TraceRepository, DocumentRepository
from services.orchestration.engine import OrchestrationEngine
from services.retrieval.service import RetrievalService
from services.speech.service import SpeechService
from shared.config.settings import get_settings


_settings = get_settings()
_cache = RedisCache(_settings.redis_url)
_document_repository = DocumentRepository.from_settings(_settings)
_trace_repository = TraceRepository.from_settings(_settings)
_retrieval_service = RetrievalService(repository=_document_repository)
_speech_service = SpeechService(
    settings=_settings,
    provider_name="openai" if _settings.openai_api_key else "mock",
)
_engine = OrchestrationEngine(
    retrieval_service=_retrieval_service,
    cache=_cache,
    trace_repository=_trace_repository,
    settings=_settings,
)


def get_engine() -> OrchestrationEngine:
    return _engine


def get_document_repository() -> DocumentRepository:
    return _document_repository


def get_trace_repository() -> TraceRepository:
    return _trace_repository


def get_speech_service() -> SpeechService:
    return _speech_service
