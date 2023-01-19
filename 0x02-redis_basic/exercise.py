#!/usr/bin/env python3
"""
Module that defies redis functionalities
"""
import uuid
import redis
from typing import Union, Callable, Optional
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """
    Counts the number of times a function is called
    Args:
        method: The function to be decorated
    Returns:
        The decorated function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function for the decorated function
        Args:
            self: The object instance
            *args: The arguments passed to the function
            **kwargs: The keyword arguments passed to the function
        Returns:
            The return value of the decorated function
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Counts the number of times a function is called
    Args:
        method: The function to be decorated
    Returns:
        The decorated function
    """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function for the decorated function
        Args:
            self: The object instance
            *args: The arguments passed to the function
            **kwargs: The keyword arguments passed to the function
        Returns:
            The return value of the decorated function
        """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data

    return wrapper


def replay(method: Callable) -> None:
    """
    Replays the history of a function
    Args:
        method: The function to be decorated
    Returns:
        None
    """
    name = method.__qualname__
    cache = redis.Redis()
    calls = cache.get(name).decode("utf-8")
    print("{} was called {} times:".format(name, calls))
    inputs = cache.lrange(name + ":inputs", 0, -1)
    outputs = cache.lrange(name + ":outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(name, i.decode('utf-8'),
                                     o.decode('utf-8')))

class Cache:
    """
    Defines methods to handle redis cache operations
    """
    def __init__(self) -> None:
        """
        Initialize redis client
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in redis cache
        """
    
        key = str(uuid. uuid4())
        self._redis.set(key, data)
        return (key)

    def get(self, key: str, fn: Optional[Callable] = None)\
        -> Union[str, bytes, int, float, None]:
        """
        Method to convert data back to desired format
        from redis cache
        """
        data = self._redis.get(key)
        if data is not None and fn is not None and callable(fn):
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Parametrizes Cache.get with correct conversion function
        """


    def get_int(self, key: str) -> int:
        """
        Parametrizes Cache.get with correct conversion function
        """
        data = self
