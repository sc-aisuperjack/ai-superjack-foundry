def build_chat_cache_key(provider: str, query: str) -> str:
    return f"chat:{provider}:{query.strip().lower()}"
