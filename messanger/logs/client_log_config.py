import logging
import sys

LOGGER = logging.getLogger('client')

FILE_HANDLER = logging.FileHandler("logs/client.log", encoding='utf-8')

STREAM_HANDLER = logging.StreamHandler(sys.stderr)

FORMATTER = logging.Formatter("%(asctime)s - %(levelname)-8s - %(module)s - %(message)s")

FILE_HANDLER.setFormatter(FORMATTER)
STREAM_HANDLER.setFormatter(FORMATTER)

LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.setLevel(logging.INFO)


if __name__ == '__main__':
    # Logger test
    LOGGER.info('Client logger test')
    LOGGER.debug('Client logger debug')
