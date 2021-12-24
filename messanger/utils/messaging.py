import json
from abc import ABC, abstractmethod

from .decorators import Log
from .constants import MAX_PACKAGE_LENGTH, ENCODING, DEFAULT_PORT, DEFAULT_IP_ADDRESS, DEFAULT_MODE


class Messaging(ABC):
    """
    Process incoming and outgoing messages

    Attributes:
        max_package_length: int, buffer size
        encoding: str, encoding type

    Methods:
        get_message(sender): decode incoming message
        send_message(recipient, message): encode and send message
    Abstract method:
        parse_message(message): parse incoming message
    Static Methods:
        get_address(argv) extract ip address from sys args
        get_port(argv): extract port from sys args
    """

    def __init__(self, max_package_length=MAX_PACKAGE_LENGTH, encoding=ENCODING):
        self.max_package_length = max_package_length
        self.encoding = encoding

    @Log()
    def get_message(self, sender):
        encoded_response = sender.recv(self.max_package_length)
        if isinstance(encoded_response, bytes):
            if len(encoded_response) == 0:
                return ''
            json_response = encoded_response.decode(self.encoding)
            response = json.loads(json_response)
            if isinstance(response, dict):
                return response
            raise ValueError
        raise ValueError

    @Log()
    def send_message(self, recipient, message):
        json_message = json.dumps(message)
        encoded_message = json_message.encode(self.encoding)
        recipient.send(encoded_message)

    @abstractmethod
    def parse_message(self, message):
        """Process incoming message"""
        pass

    @staticmethod
    def get_address(argv=[]):
        try:
            if '-a' in argv:
                address = argv[argv.index('-a') + 1]
            else:
                address = DEFAULT_IP_ADDRESS
            return address, 'ok'
        except IndexError:
            return -1, 'Incorrect IP address'

    @staticmethod
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


    @staticmethod
    def get_name(argv=[]):
        try:
            if '-n' in argv:
                name = argv[argv.index('-n') + 1]
            else:
                name = 'Guest'
            return name, 'ok'
        except IndexError:
            return -1, 'Incorrect name value.'
