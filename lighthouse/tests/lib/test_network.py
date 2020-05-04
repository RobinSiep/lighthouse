from unittest import TestCase

from lighthouse.lib.network import network_addr_to_binary_string


class TestNetworkAddrToBinaryString(TestCase):
    def test_ip_address(self):
        binary_addr = network_addr_to_binary_string("192.168.178.41")
        self.assertEqual(binary_addr, "11000000101010001011001000101001")

    def test_invalid_address(self):
        pass
