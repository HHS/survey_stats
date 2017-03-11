"""Global LRU caching utility. For that little bit of extra speed.

The caching utility provides a single wrapper function that can be used to
provide a bit of extra speed for some often used function. The cache is an LRU
cache including a key timeout.

Usage::

	import cache
	@cache.memoize
	def myfun(x, y):
		return x + y


Also support asyncio coroutines::

	@cache.memoize
	async def myfun(x, y):
		x_result = await fetch_x(x)
		return x_result + y


The cache can be manually cleared with `myfun.cache.clear()`

"""
import asyncio
import uvloop
import ujson as json
from functools import wraps, partial
from cachetools.keys import hashkey
from lru import LRUCacheDict

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

__all__ = ['memoize']


def _wrap_coroutine_storage(cache_dict, key, future):
    async def wrapper():
        val = await future
        cache_dict[key] = val
        return val
    return wrapper()


def _wrap_value_in_coroutine(val):
    async def wrapper():
        return val
    return wrapper()


def memoize(f=None,key_fn=hashkey):
    """An in-memory cache wrapper that can be used on any function, including
    coroutines.

    """
    __cache = LRUCacheDict(max_size=65536, expiration=86400)
    if f is None:
       return partial(memoize, key_fn=key_fn)
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Simple key generation. Notice that there are no guarantees that the
        # key will be the same when using dict arguments.
        key = f.__module__ + '#' + f.__name__ + '#' + json.dumps(key_fn(*args, **kwargs))
        try:
            val = __cache[key]
            if asyncio.iscoroutinefunction(f):
                return _wrap_value_in_coroutine(val)
            return val
        except KeyError:
            val = f(*args, **kwargs)

            if asyncio.iscoroutine(val):
                # If the value returned by the function is a coroutine, wrap
                # the future in a new coroutine that stores the actual result
                # in the cache.
                return _wrap_coroutine_storage(__cache, key, val)

            # Otherwise just store and return the value directly
            __cache[key] = val
            return val

    return wrapper
