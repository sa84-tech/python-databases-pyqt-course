from .constants import MAX_PACKAGE_LENGTH, ENCODING, DEFAULT_PORT, DEFAULT_IP_ADDRESS, DEFAULT_MODE


def get_address(argv=[]):
    try:
        if '-a' in argv:
            address = argv[argv.index('-a') + 1]
        else:
            address = DEFAULT_IP_ADDRESS
        return address, 'ok'
    except IndexError:
        return -1, 'Incorrect IP address'


def get_port(argv=[]):
    try:
        if '-p' in argv:
            port = int(argv[argv.index('-p') + 1])
            # if not 1024 <= port <= 65535:
            #     raise ValueError
        else:
            port = DEFAULT_PORT
        return port, 'ok'
    except ValueError:
        return -1, 'Valid port range: 1024-65535'
    except IndexError:
        return -1, 'Incorrect port number'


def get_name(argv=[]):
    try:
        if '-n' in argv:
            name = argv[argv.index('-n') + 1]
        else:
            name = 'Guest'
        return name, 'ok'
    except IndexError:
        return -1, 'Incorrect name value.'
