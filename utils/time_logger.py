import logging
from functools import wraps
from time import time


def time_logger(func):
    @wraps(func)
    def time_wrapper(*args, **kwargs):
        start = time()
        res = func(*args, **kwargs)
        duration = (time() - start) * 1000  # milliseconds
        logging.info(f"{func.__module__}.{func.__name__} took {duration :.2f} milliseconds to execute.")

        return res

    return time_wrapper

