from services.llm_router.base import BaseLLMProvider
from services.llm_router.providers import AnthropicProvider, GeminiProvider, MockLLMProvider, OpenAIProvider
from shared.config.settings import Settings


def get_llm_provider(provider_name: str, settings: Settings) -> BaseLLMProvider:
    normalized = (provider_name or settings.default_llm_provider or "mock").strip().lower()
    providers: dict[str, BaseLLMProvider] = {
        "mock": MockLLMProvider(),
        "openai": OpenAIProvider(settings=settings),
        "anthropic": AnthropicProvider(),
        "gemini": GeminiProvider(),
    }
    return providers.get(normalized, MockLLMProvider())
