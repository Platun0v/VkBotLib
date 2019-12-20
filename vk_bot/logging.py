import logging.handlers


LEVEL = logging.INFO
FORMAT = logging.Formatter('%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)d) - %(name)s: "%(message)s"')

file_handler = logging.FileHandler('bot.log')
file_handler.setLevel(LEVEL)
file_handler.setFormatter(FORMAT)

console_handler = logging.StreamHandler()
console_handler.setLevel(LEVEL)
console_handler.setFormatter(FORMAT)

logger = logging.Logger('bot')
logger.setLevel(LEVEL)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def set_logging_level(level):
    file_handler.setLevel(level)
    console_handler.setLevel(level)
    logger.setLevel(level)
