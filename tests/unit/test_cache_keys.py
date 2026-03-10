from shared.utils.cache_keys import build_chat_cache_key


def test_build_chat_cache_key_normalises_query() -> None:
    assert build_chat_cache_key("mock", "  Hello World  ") == "chat:mock:hello world"
