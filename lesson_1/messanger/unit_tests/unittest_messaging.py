import os
import sys
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))
from utils.messaging import Messaging
from utils.constants import DEFAULT_PORT, DEFAULT_IP_ADDRESS


class TestMessaging(unittest.TestCase):
    def test_get_port(self):
        port = Messaging.get_port(['-p', '5000'])
        self.assertEqual(port, 5000)

    def test_get_port_default(self):
        port = Messaging.get_port()
        self.assertEqual(port, DEFAULT_PORT)

    def test_get_port_out_range(self):
        port = Messaging.get_port(['-p', '1000'])
        self.assertEqual(port, -1)

    def test_get_address(self):
        address = Messaging.get_address(['-a', '192.168.0.1'])
        self.assertEqual(address, '192.168.0.1')

    def test_get_address_default(self):
        address = Messaging.get_address()
        self.assertEqual(address, DEFAULT_IP_ADDRESS)

    def test_get_address_incorrect_args(self):
        address = Messaging.get_address(['-a'])
        self.assertEqual(address, -1)


if __name__ == "__main__":
    unittest.main()
