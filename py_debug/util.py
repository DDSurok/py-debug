from datetime import datetime
import logging
import functools


__call_counters = {}


def log_running_time(func, level: int = logging.DEBUG):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.now()
        res = func(*args, **kwargs)
        if not logging.getLevelName(level).startswith('Level '):
            logging.log(level, f'The call [{func.__name__}] is completed in {(datetime.now()-start).total_seconds()}.')
        else:
            logging.warning('Log level has not found.')
        return res
    return wrapper


def log_args(func, level: int = logging.DEBUG):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not logging.getLevelName(level).startswith('Level '):
            logging.log(level, f'Call {func.__name__} with {args = } and {kwargs = }.')
        else:
            logging.warning('Log level has not found.')
        res = func(*args, **kwargs)
        return res
    return wrapper


def call_counter(func, level: int = logging.DEBUG, mute_after: int = 5, log_every: int = 10):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if func.__name__ in __call_counters:
            __call_counters[func.__name__] += 1
        else:
            __call_counters[func.__name__] = 1
        if __call_counters[func.__name__] - 1 in range(mute_after) or not __call_counters[func.__name__] % log_every:
            if not logging.getLevelName(level).startswith('Level '):
                logging.log(level, f'Function {func.__name__} has been called {__call_counters[func.__name__]} times.')
            else:
                (logging.warning('Log level has not found.'))
        res = func(*args, **kwargs)
        return res

    return wrapper


__all__ = [
    "log_running_time",
    "log_args",
    "call_counter",
]
