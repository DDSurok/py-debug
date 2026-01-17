"""
    Py-debug: Simple logging decorators for Python functions.
    Functions for logging function calls, execution time, and call counts.
"""
import logging
import time
from functools import wraps
from typing import Callable, Any, Dict, Optional
from threading import Lock

# Thread-safe call counter storage
_call_counters: Dict[str, int] = {}
_counter_lock = Lock()


def _is_valid_log_level(level: int) -> bool:
    """
    Check if a log level is valid.

    Args:
        level: The log level to validate.

    Returns:
        True if the level is valid, False otherwise.
    """
    try:
        # Try to get the level name - if it's a valid level, it won't start with 'Level '
        level_name = logging.getLevelName(level)
        return not level_name.startswith('Level ')
    except (TypeError, AttributeError):
        return False


def _get_function_name(func: Callable) -> str:
    """
    Get the full qualified name of a function.

    Args:
        func: The function to get the name for.

    Returns:
        The full qualified name (module.function_name).
    """
    return f'{func.__module__}.{func.__name__}'


def _format_args_info(args: tuple, kwargs: dict) -> str:
    """
    Format function arguments for logging.

    Args:
        args: Positional arguments.
        kwargs: Keyword arguments.

    Returns:
        A formatted string describing the arguments.
    """
    if not args and not kwargs:
        return 'without args'
    elif args and not kwargs:
        return f'with {args = }'
    elif not args and kwargs:
        return f'with {kwargs = }'
    else:
        return f'{args = } and {kwargs = }'


def log_running_time(level: int = logging.DEBUG) -> Callable:
    """
    Decorator to log the execution time of a function.

    Args:
        level: The logging level to use (default: logging.DEBUG).

    Returns:
        A decorator function.

    Example:
        >>> import logging
        >>> logging.basicConfig(level=logging.DEBUG)
        >>>
        >>> @log_running_time()
        ... def my_function():
        ...     time.sleep(0.1)
        ...     return 42
        >>>
        >>> result = my_function()  # Logs execution time
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            full_name = _get_function_name(func)
            start_time = time.perf_counter()

            try:
                result = func(*args, **kwargs)
                elapsed_time = time.perf_counter() - start_time

                if _is_valid_log_level(level):
                    logging.log(
                        level,
                        f'The call [{full_name}] is completed in {elapsed_time:.6f} seconds.'
                    )
                else:
                    logging.warning(f'Invalid log level {level} for function {full_name}.')

                return result
            except Exception as e:
                elapsed_time = time.perf_counter() - start_time
                if _is_valid_log_level(level):
                    logging.log(
                        level,
                        f'The call [{full_name}] failed after {elapsed_time:.6f} seconds: {type(e).__name__}: {e}'
                    )
                else:
                    logging.warning(f'Invalid log level {level} for function {full_name}.')
                raise

        return wrapper

    return decorator


def log_args(level: int = logging.DEBUG) -> Callable:
    """
    Decorator to log the arguments passed to a function.

    Args:
        level: The logging level to use (default: logging.DEBUG).

    Returns:
        A decorator function.

    Example:
        >>> import logging
        >>> logging.basicConfig(level=logging.DEBUG)
        >>>
        >>> @log_args()
        ... def add(a, b):
        ...     return a + b
        >>>
        >>> result = add(1, 2)  # Logs: Function add has been called with args = (1, 2).
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            full_name = _get_function_name(func)

            if _is_valid_log_level(level):
                args_info = _format_args_info(args, kwargs)
                logging.log(level, f'Function {full_name} has been called {args_info}.')
            else:
                logging.warning(f'Invalid log level {level} for function {full_name}.')

            return func(*args, **kwargs)

        return wrapper

    return decorator


def log_call_counter(level: int = logging.DEBUG, mute_after: int = 5, log_every: int = 10) -> Callable:
    """
    Decorator to log the number of times a function has been called.

    Args:
        level: The logging level to use (default: logging.DEBUG).
        mute_after: Number of initial calls to log before muting (default: 5).
        log_every: Log every Nth call after muting (default: 10).

    Returns:
        A decorator function.

    Example:
        >>> import logging
        >>> logging.basicConfig(level=logging.DEBUG)
        >>>
        >>> @log_call_counter(mute_after=2, log_every=5)
        ... def my_function():
        ...     return True
        >>>
        >>> for i in range(20):
        ...     my_function()  # Logs first 2 calls, then every 5th call
    """
    if mute_after < 0:
        raise ValueError("mute_after must be non-negative")
    if log_every < 1:
        raise ValueError("log_every must be positive")

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            full_name = _get_function_name(func)

            # Thread-safe counter increment
            with _counter_lock:
                if full_name in _call_counters:
                    _call_counters[full_name] += 1
                else:
                    _call_counters[full_name] = 1
                call_count = _call_counters[full_name]

            # Determine if we should log this call
            should_log = (
                    (call_count - 1) < mute_after or  # First mute_after calls
                    call_count % log_every == 0  # Every log_every calls
            )

            if should_log:
                if _is_valid_log_level(level):
                    logging.log(
                        level,
                        f'Function {full_name} has been called {call_count} times.'
                    )
                else:
                    logging.warning(f'Invalid log level {level} for function {full_name}.')

            try:
                return func(*args, **kwargs)
            except Exception:
                # If log level is invalid, log warning even if should_log is False
                if not _is_valid_log_level(level) and not should_log:
                    logging.warning(f'Invalid log level {level} for function {full_name}.')
                raise

        return wrapper

    return decorator


def reset_call_counters() -> None:
    """
    Reset all function call counters.

    This is useful for testing or when you want to reset the counters
    without restarting the application.

    Example:
        >>> from py_debug import reset_call_counters
        >>> reset_call_counters()  # Clears all counters
    """
    with _counter_lock:
        _call_counters.clear()


def get_call_count(func: Callable) -> int:
    """
    Get the current call count for a function.

    Args:
        func: The function to get the count for.

    Returns:
        The number of times the function has been called, or 0 if never called.

    Example:
        >>> @log_call_counter()
        ... def my_func():
        ...     pass
        >>>
        >>> my_func()
        >>> my_func()
        >>> print(get_call_count(my_func))  # Output: 2
    """
    full_name = _get_function_name(func)
    with _counter_lock:
        return _call_counters.get(full_name, 0)


__all__ = [
    "log_running_time",
    "log_args",
    "log_call_counter",
    "reset_call_counters",
    "get_call_count",
]

__version__ = "0.1.1"
