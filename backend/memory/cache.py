from typing import Dict, Any
import asyncio

_cache: Dict[str, Any] = {}
_lock = asyncio.Lock()

async def set_cache(key: str, value: Any):
    async with _lock:
        _cache[key] = value

async def get_cache(key: str):
    async with _lock:
        return _cache.get(key)
