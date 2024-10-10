from django.core.cache import cache


def comments_cache_dec(func):
    def wrapper(*args):
        key = f"comments({int(args[0])})"
        val = cache.get(key)
        if val is None:
            val = func(*args)
            cache.set(key, val)
        return val

    return wrapper

def comments_cache_invalidate(post_id):
    cache.delete(f"comments({post_id})")