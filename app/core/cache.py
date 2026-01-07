# app/core/cache.py

import time

CACHE_TTL_SECONDS = 60 * 60  # 1 hour

_cache = {}

def get_cached_response(query: str):
    entry = _cache.get(query)
    if not entry:
        return None

    value, timestamp = entry
    if time.time() - timestamp > CACHE_TTL_SECONDS:
        del _cache[query]
        return None

    return value


def set_cached_response(query: str, response: dict):
    _cache[query] = (response, time.time())
