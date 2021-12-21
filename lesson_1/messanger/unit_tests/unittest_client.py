import os
import sys
import unittest
import json

sys.path.append(os.path.join(os.getcwd(), '..'))
from client import Client
from utils.constants import DEFAULT_PORT, DEFAULT_IP_ADDRESS, RESPONSE_DEFAULT_IP_ADDRESS, ERROR, ACTION, PRESENCE, \
    TIME, USER, ACCOUNT_NAME, RESPONSE, ENCODING


class TestSocket:
    def __init__(self, message):
        self.message = message

    def recv(self, max_package_length):
        json_message = json.dumps(self.message)
        encoded_message = json_message.encode(ENCODING)
        return encoded_message


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = Client(DEFAULT_IP_ADDRESS, DEFAULT_PORT)

    def tearDown(self):
        self.client.socket.close()

    def test_get_port(self):
        self.assertEqual(self.client.srv_port, DEFAULT_PORT)

    def test_get_address(self):
        self.assertEqual(self.client.srv_address, DEFAULT_IP_ADDRESS)

    def test_create_init_message(self):
        account_name = self.client.create_init_message()[USER][ACCOUNT_NAME]
        self.assertEqual(account_name, 'Guest')

    def test_parse_message(self):
        message = {RESPONSE: 200}
        self.assertEqual(self.client.parse_message(message), '200 : OK')

    def test_parse_message_err_code(self):
        message = {RESPONSE: 400, ERROR: 'Bad request'}
        self.assertEqual(self.client.parse_message(message), '400 : Bad request')

    def test_parse_message_exception(self):
        self.assertRaises(ValueError, self.client.parse_message, {})

    def test_get_message(self):
        test_socket = TestSocket({RESPONSE: 200})
        self.assertEqual(self.client.get_message(test_socket), {RESPONSE: 200})

    def test_get_message_exception(self):
        test_socket = TestSocket('')
        self.assertRaises(ValueError, self.client.get_message, test_socket)


if __name__ == "__main__":
    unittest.main()
