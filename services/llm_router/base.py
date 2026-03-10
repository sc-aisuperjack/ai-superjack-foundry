from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    provider_name: str = "base"

    @abstractmethod
    async def answer(self, query: str, context_chunks: list[str]) -> str:
        raise NotImplementedError
