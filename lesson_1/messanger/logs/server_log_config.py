import logging
import sys
from logging import handlers

LOGGER = logging.getLogger('server')

FILE_HANDLER = handlers.TimedRotatingFileHandler("logs/server.log", "D", 1, 7, encoding='utf-8')

STREAM_HANDLER = logging.StreamHandler(sys.stderr)

FORMATTER = logging.Formatter("%(asctime)s - %(levelname)-8s - %(module)s - %(message)s")

FILE_HANDLER.setFormatter(FORMATTER)
STREAM_HANDLER.setFormatter(FORMATTER)

LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.setLevel(logging.INFO)


if __name__ == '__main__':
    # Logger test
    LOGGER.info('Logger test')
    LOGGER.debug('Server logger debug')
