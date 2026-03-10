import asyncio
from typing import Sequence

from openai import OpenAI

from services.llm_router.base import BaseLLMProvider
from shared.config.settings import Settings


class MockLLMProvider(BaseLLMProvider):
    provider_name = "mock"

    async def answer(self, query: str, context_chunks: list[str]) -> str:
        context = " ".join(context_chunks[:2]).strip()
        if context:
            return f"Grounded answer: {context} | User asked: {query}"
        return f"Mock answer generated for query: {query}"


class OpenAIProvider(BaseLLMProvider):
    provider_name = "openai"

    def __init__(self, settings: Settings):
        self.settings = settings

    async def answer(self, query: str, context_chunks: list[str]) -> str:
        if not self.settings.openai_api_key:
            return await MockLLMProvider().answer(query=query, context_chunks=context_chunks)

        return await asyncio.to_thread(self._answer_sync, query, context_chunks)

    def _answer_sync(self, query: str, context_chunks: Sequence[str]) -> str:
        client = OpenAI(api_key=self.settings.openai_api_key)
        context = "\n\n".join(context_chunks[:4]).strip() or "No grounded context available."
        system_prompt = (
            "You are a grounded AI copilot. Use the provided context first. "
            "If context is insufficient, say so plainly. Keep answers concise and factual."
        )
        response = client.responses.create(
            model=self.settings.openai_chat_model,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{query}"},
            ],
        )
        text = getattr(response, "output_text", "") or ""
        return text.strip() or "The model returned an empty response."


class AnthropicProvider(MockLLMProvider):
    provider_name = "anthropic"


class GeminiProvider(MockLLMProvider):
    provider_name = "gemini"
