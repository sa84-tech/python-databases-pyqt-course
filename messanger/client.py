import logging
import sys
import socket
import json
import time
import threading

from utils.decorators import Log
from utils.constants import DEFAULT_PORT, DEFAULT_IP_ADDRESS, RESPONSE, ERROR, ACTION, PRESENCE, TIME, USER, \
    MESSAGE, SENDER, RECIPIENT, EXIT, ACCOUNT_NAME, ALERT, CODE, ENCODING, MAX_PACKAGE_LENGTH, MESSAGE_TEXT
from utils.messaging import get_address, get_port, get_name
from utils.descriptors import CheckPort

from utils.metaclasses import ClientVerifier


class Client(metaclass=ClientVerifier):
    srv_port = CheckPort()
    encoding = ENCODING
    max_package_length = MAX_PACKAGE_LENGTH

    def __init__(self, sock, srv_address=DEFAULT_IP_ADDRESS, srv_port=DEFAULT_PORT, account_name='Guest'):
        self.srv_address = srv_address
        self.srv_port = srv_port
        self.account_name = account_name
        self.sock = sock
        self.logger = logging.getLogger('client')
        self.is_exit = False

    def __str__(self):
        return f'Client {self.account_name}) ' \
               f'is connected to {self.srv_address}:{self.srv_port}'

    # @Log()
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

    # @Log()
    def send_message(self, recipient, message):
        json_message = json.dumps(message)
        encoded_message = json_message.encode(self.encoding)
        recipient.send(encoded_message)

    # @Log()
    def parse_message(self, message):
        if CODE in message:
            if message[CODE] == 200:
                return message[ALERT], message[CODE]
            self.logger.warning(f'RESPONSE FROM SERVER: {message[CODE]} : {message[ERROR]}')
            return message[ERROR], message[CODE]
        elif ACTION in message and message[ACTION] == MESSAGE:
            self.logger.info(f'Incoming message from: {message[SENDER]}')
            return f'\nIncoming message from {message[SENDER]}:\n{message[MESSAGE_TEXT]}', 200
        raise ValueError

    # @Log()
    def create_init_message(self):
        message = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: self.account_name
            }
        }
        return message

    # @Log()
    def create_message(self):
        recipient = input('Enter recipient: ')
        text = input('Enter message: ')
        message = {
            ACTION: MESSAGE,
            TIME: time.time(),
            SENDER: self.account_name,
            RECIPIENT: recipient,
            MESSAGE_TEXT: text
        }
        return message

    # @Log()
    def create_final_message(self):
        message = {
            ACTION: EXIT,
            TIME: time.time(),
            SENDER: self.account_name,
        }
        return message

    # @Log()
    def start_sending_mode(self):
        while True:
            command = input('Select action, m - send message, q - exit: ')
            if command == 'm':
                message = self.create_message()
                try:
                    self.send_message(self.sock, message)
                    print(f'Message sent to {message[RECIPIENT]}')
                except ConnectionError:
                    self.logger.error(f'Connection with server {self.srv_address} lost.')
                    sys.exit(1)
            elif command == 'q':
                try:
                    self.shutdown()
                except ConnectionError:
                    self.logger.error(f'Connection with server {self.srv_address} lost.')
                    break
            else:
                print("Unknown command")

            time.sleep(0.5)

    # @Log()
    def start_reception_mode(self):
        while True:
            try:
                res = self.get_message(self.sock)
                if res:
                    in_message, code = self.parse_message(res)
                    print(in_message)
            except ConnectionError:
                if self.is_exit:
                    time.sleep(1)
                    break
                self.logger.error(f'Connection with server {self.srv_address} lost.')
                sys.exit(1)
            except (ValueError, json.JSONDecodeError):
                self.logger.error('Failed to decode server message')
                break

    # @Log()
    def register(self):
        while True:
            init_message = self.create_init_message()
            self.send_message(self.sock, init_message)
            message = self.get_message(self.sock)
            response, code = self.parse_message(message)
            if code == 200:
                print(f'Connection established, Server: {self.sock.getpeername()}, '
                      f'Client: {self.sock.getsockname()}')
                print('Response from Server: ', response)
                break
            else:
                while True:
                    print('Response from Server:', message[ERROR])
                    choice = input('Select action, n - new name, q - quit the chat: ')
                    if choice == 'q':
                        self.shutdown()
                    if choice == 'n':
                        new_name = input('Enter new name: ')
                        self.account_name = new_name
                        break
                    else:
                        print('Unknown command')

    # @Log()
    def shutdown(self):
        self.is_exit = True
        self.send_message(self.sock, self.create_final_message())
        self.sock.shutdown(socket.SHUT_RDWR)
        self.logger.info('Shutdown by user command')
        print('Bye')
        time.sleep(0.5)
        sys.exit(0)

    # @Log()
    def connect(self):
        try:
            self.sock.connect((self.srv_address, self.srv_port))
            self.logger.info(self)
            self.register()
        except ConnectionError:
            self.logger.error('Connection failed')
        except (ValueError, json.JSONDecodeError):
            self.logger.error('Failed to decode server message')
        else:

            receiver = threading.Thread(target=self.start_reception_mode)
            receiver.daemon = True
            receiver.start()

            sender = threading.Thread(target=self.start_sending_mode)
            sender.daemon = True
            sender.start()
            self.logger.debug('Messaging process started')

            while True:
                time.sleep(1)
                if receiver.is_alive() and sender.is_alive():
                    continue
                break


@Log()
def check_error(value, message, logger):
    if value == -1:
        logger.critical(message)
        sys.exit(1)
    return value


@Log()
def main():
    logger = logging.getLogger('client')

    address = check_error(*get_address(sys.argv), logger=logger)
    port = check_error(*get_port(sys.argv), logger=logger)
    name = check_error(*get_name(sys.argv), logger=logger)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client = Client(sock, srv_address=address, srv_port=port, account_name=name)
    client.connect()


if __name__ == '__main__':
    main()
