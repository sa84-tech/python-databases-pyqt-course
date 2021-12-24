import logging
import sys
import socket
import json
import time
import threading

from utils.decorators import Log
from utils.constants import DEFAULT_PORT, DEFAULT_IP_ADDRESS, RESPONSE, ERROR, ACTION, PRESENCE, TIME, USER, \
    MESSAGE, SENDER, RECIPIENT, EXIT, ACCOUNT_NAME, ALERT, CODE
from utils.messaging import Messaging
from utils.descriptors import CheckPort

from messanger.utils.constants import MESSAGE, MESSAGE_TEXT


class Client(Messaging):
    srv_port = CheckPort()

    def __init__(self, srv_address=DEFAULT_IP_ADDRESS, srv_port=DEFAULT_PORT, account_name='Guest'):
        super().__init__()
        self.srv_address = srv_address
        self.srv_port = srv_port
        self.account_name = account_name
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger = logging.getLogger('client')
        self.is_exit = False

    def __str__(self):
        return f'Client ({socket.gethostname()}, name: {self.account_name}) ' \
               f'is connected to {self.srv_address}:{self.srv_port}'

    @Log()
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

    @Log()
    def create_init_message(self):
        message = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: self.account_name
            }
        }
        return message

    @Log()
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

    @Log()
    def create_final_message(self):
        message = {
            ACTION: EXIT,
            TIME: time.time(),
            SENDER: self.account_name,
        }
        return message

    @Log()
    def start_sending_mode(self):
        while True:
            command = input('Select action, m - send message, q - exit: ')
            if command == 'm':
                message = self.create_message()
                try:
                    self.send_message(self.socket, message)
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

    @Log()
    def start_reception_mode(self):
        while True:
            try:
                res = self.get_message(self.socket)
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

    @Log()
    def register(self):
        while True:
            init_message = self.create_init_message()
            self.send_message(self.socket, init_message)
            message = self.get_message(self.socket)
            response, code = self.parse_message(message)
            if code == 200:
                print(f'Connection established, Server: {self.socket.getpeername()}, '
                      f'Client: {self.socket.getsockname()}')
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

    @Log()
    def shutdown(self):
        self.is_exit = True
        self.send_message(self.socket, self.create_final_message())
        self.socket.shutdown(socket.SHUT_RDWR)
        self.logger.info('Shutdown by user command')
        print('Bye')
        time.sleep(0.5)
        sys.exit(0)

    @Log()
    def connect(self):
        try:
            self.socket.connect((self.srv_address, self.srv_port))
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


if __name__ == '__main__':
    def check_error(value, message):
        if value == -1:
            logger.critical(message)
            sys.exit(1)
        return value


    logger = logging.getLogger('client')

    address = check_error(*Messaging.get_address(sys.argv))
    port = check_error(*Messaging.get_port(sys.argv))
    name = check_error(*Messaging.get_name(sys.argv))

    client = Client(srv_address=address, srv_port=port, account_name=name)
    client.connect()
