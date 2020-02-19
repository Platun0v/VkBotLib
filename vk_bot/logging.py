import logging.handlers
import functools


LEVEL = logging.INFO
FORMAT = logging.Formatter('%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)d) - %(name)s: "%(message)s"')

logger = logging.Logger('bot')
logger.setLevel(LEVEL)

file_handler = logging.FileHandler('bot.log')
console_handler = logging.StreamHandler()
is_standard_handlers_used = False


def set_logging_level(level):
    if is_standard_handlers_used:
        file_handler.setLevel(level)
        console_handler.setLevel(level)
    logger.setLevel(level)


def log(func):
    dec_logger = logging.getLogger(func.__module__)

    @functools.wraps(func)
    def decorator(self, *args, **kwargs):
        dec_logger.debug('Entering: %s', func.__name__)
        result = func(self, *args, **kwargs)
        dec_logger.debug(result)
        dec_logger.debug('Exiting: %s', func.__name__)
        return result

    return decorator


def init_standard_logging_handlers():
    global is_standard_handlers_used
    is_standard_handlers_used = True
    file_handler.setLevel(LEVEL)
    file_handler.setFormatter(FORMAT)

    console_handler.setLevel(LEVEL)
    console_handler.setFormatter(FORMAT)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
