import os
import sys
import logging
import traceback

sys.path.append(os.path.join(os.getcwd(), '..'))
import logs.server_log_config
import logs.client_log_config

if sys.argv[0].find('client') == -1:
    LOGGER = logging.getLogger('server')
else:
    LOGGER = logging.getLogger('client')


class Log:
    def __call__(self, func):
        def decorated(*args, **kwargs):
            res = func(*args, **kwargs)
            LOGGER.debug(f'Function: {func.__name__}. Args: {args}, {kwargs}. '
                         f'Call from module: {func.__module__}. '
                         f'Call from function: {traceback.format_stack()[0].strip().split()[-1]}. ')
            return res
        return decorated
