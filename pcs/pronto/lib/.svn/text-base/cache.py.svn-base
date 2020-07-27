from django.core.cache import cache
from django.core.cache import caches
from django.core.cache import DEFAULT_CACHE_ALIAS


def get_cache(cache_key):
    return cache.get(cache_key)


def set_cache(cache_key, cache_content):
    cache.set(cache_key, cache_content, 60 * 30)


def clear_cache():
    caches[DEFAULT_CACHE_ALIAS].clear()
