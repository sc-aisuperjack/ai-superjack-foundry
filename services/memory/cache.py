import json
from typing import Any

from redis import Redis


class RedisCache:
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        try:
            self.client = Redis.from_url(redis_url, decode_responses=True)
            self.client.ping()
            self.available = True
        except Exception:
            self.client = None
            self.available = False
            self._fallback: dict[str, str] = {}

    def get_json(self, key: str) -> dict[str, Any] | None:
        raw = self.client.get(key) if self.available and self.client else self._fallback.get(key)
        return json.loads(raw) if raw else None

    def set_json(self, key: str, value: dict[str, Any], ttl_seconds: int = 300) -> None:
        payload = json.dumps(value)
        if self.available and self.client:
            self.client.setex(key, ttl_seconds, payload)
        else:
            self._fallback[key] = payload
