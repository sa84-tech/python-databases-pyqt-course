import os
import sys
import unittest
from datetime import time

sys.path.append(os.path.join(os.getcwd(), '..'))
from server import Server
from utils.constants import DEFAULT_PORT, DEFAULT_IP_ADDRESS, RESPONSE_DEFAULT_IP_ADDRESS, ERROR, ACTION, PRESENCE, \
    TIME, USER, ACCOUNT_NAME, RESPONSE


class TestServer(unittest.TestCase):
    def setUp(self):
        self.server = Server()

    def tearDown(self):
        self.server.socket.close()

    def test_get_port(self):
        self.assertEqual(self.server.port, DEFAULT_PORT)

    def test_request(self):
        message = {
            ACTION: PRESENCE,
            TIME: 123,
            USER: {
                ACCOUNT_NAME: 'Guest'
            }
        }
        self.assertDictEqual(self.server.parse_message(message), {RESPONSE: 200})

    def test_bad_request(self):
        response = {
            RESPONSE_DEFAULT_IP_ADDRESS: 400,
            ERROR: 'Bad Request'
        }
        self.assertDictEqual(self.server.parse_message({}), response)


if __name__ == "__main__":
    unittest.main()
