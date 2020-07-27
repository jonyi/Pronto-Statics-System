from .cache import get_cache, set_cache


def wrapper_cache(func):
    def new_func(*args):
        cache_key = func.__name__
        old_cache = get_cache(cache_key)
        if old_cache:
            return old_cache
        else:
            new_cache = func(*args)
            set_cache(cache_key, func(*args))
            return new_cache
    return new_func


def wrapper_cache_with_param(func):
    def new_func(*args):
        cache_key = func.__name__ + args[0]
        old_cache = get_cache(cache_key)
        if old_cache:
            return old_cache
        else:
            new_cache = func(*args)
            set_cache(cache_key, func(*args))
            return new_cache
    return new_func

