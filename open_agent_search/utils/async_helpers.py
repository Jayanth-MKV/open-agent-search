"""
Utility functions for async operations
"""

import asyncio
from functools import partial, wraps
from typing import Any, Callable


async def run_in_threadpool(func: Callable, *args, **kwargs) -> Any:
    """
    Run a blocking/synchronous function in a thread pool.

    This prevents blocking the async event loop when calling synchronous libraries
    like DDGS that perform blocking I/O operations.

    Args:
        func: The synchronous function to run
        *args: Positional arguments for the function
        **kwargs: Keyword arguments for the function

    Returns:
        The result of the function call

    Example:
        result = await run_in_threadpool(search_text, query="python", max_results=10)
    """
    loop = asyncio.get_running_loop()

    # If function has kwargs, use partial to bind them
    if kwargs:
        func_with_args = partial(func, *args, **kwargs)
        return await loop.run_in_executor(None, func_with_args)
    else:
        func_with_args = partial(func, *args) if args else func
        return await loop.run_in_executor(None, func_with_args)


def async_wrap(func: Callable) -> Callable:
    """
    Decorator to automatically wrap a synchronous function to run in a thread pool.

    Usage:
        @async_wrap
        def blocking_function(arg1, arg2):
            # ... blocking code ...
            return result

        # Can now be called with await
        result = await blocking_function(val1, val2)
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        return await run_in_threadpool(func, *args, **kwargs)

    return wrapper
