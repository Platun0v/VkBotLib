import functools
import logging.handlers
import sys

LEVEL = logging.ERROR
FORMAT = logging.Formatter('%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)d) - %(name)s: "%(message)s"')

logger = logging.getLogger('vk_bot')

console_output_handler = logging.StreamHandler(sys.stderr)
console_output_handler.setFormatter(FORMAT)
logger.addHandler(console_output_handler)

logger.setLevel(LEVEL)


def log(func):
    dec_logger = logging.getLogger(func.__module__)

    @functools.wraps(func)
    def decorator(self, *args, **kwargs):
        dec_logger.debug(f'Entering: {func.__name__}')
        result = func(self, *args, **kwargs)
        dec_logger.debug(result)
        dec_logger.debug(f'Exiting: {func.__name__}')
        return result

    return decorator
