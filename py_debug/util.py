from datetime import datetime
import logging
import functools


__call_counters = {}


def log_running_time(func, level: int = logging.DEBUG):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        full_name = f'{func.__module__}.{func.__name__}'
        start = datetime.now()
        res = func(*args, **kwargs)
        if not logging.getLevelName(level).startswith('Level '):
            logging.log(level, f'The call [{full_name}] is completed in {(datetime.now()-start).total_seconds()}.')
        else:
            logging.warning('Log level has not found.')
        return res
    return wrapper


def log_args(func, level: int = logging.DEBUG):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        full_name = f'{func.__module__}.{func.__name__}'
        if not logging.getLevelName(level).startswith('Level '):
            if not len(args) and not len(kwargs):
                args_info = 'without args'
            elif len(args) and not len(kwargs):
                args_info = f'with {args = }'
            elif not len(args) and len(kwargs):
                args_info = f'with {kwargs = }'
            else:
                args_info = f'{args = } and {kwargs = }'
            logging.log(level, f'Function {full_name} has been called {args_info}.')
        else:
            logging.warning('Log level has not found.')
        res = func(*args, **kwargs)
        return res
    return wrapper


def call_counter(func, level: int = logging.DEBUG, mute_after: int = 5, log_every: int = 10):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        full_name = f'{func.__module__}.{func.__name__}'
        if full_name in __call_counters:
            __call_counters[full_name] += 1
        else:
            __call_counters[full_name] = 1
        if __call_counters[full_name] - 1 in range(mute_after) or not __call_counters[full_name] % log_every:
            if not logging.getLevelName(level).startswith('Level '):
                logging.log(level, f'Function {full_name} has been called {__call_counters[full_name]} times.')
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
