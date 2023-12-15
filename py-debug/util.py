from datetime import datetime
import logging
import functools


def log_running_time(func, level:int=logging.DEBUG):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.now()
        res = func(*args, **kwargs)
        if level in (logging.getLevelNamesMapping().values()):
            log_method = getattr(logging, logging.getLevelName(level))
            log_method(f'The call [{func.__name__}] is completed in {(datetime.now()-start).total_seconds()}.')
        else:
            logging.warning('Log level has not found.')
        return res
    return wrapper


def log_args(func, level:int=logging.WARNING):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if level in (logging.getLevelNamesMapping().values()):
            log_method = getattr(logging, logging.getLevelName(level))
            log_method(f'Call {func.__name__} with args: [{args}] and kwargs: [{kwargs}].')
        else:
            logging.warning('Log level has not found.')
        res = func(*args, **kwargs)
        return res
    return wrapper
