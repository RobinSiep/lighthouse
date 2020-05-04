from unittest import TestCase

from lighthouse.lib.network import (
    network_addr_to_binary_string, get_subnet_size, valid_subnet_mask)


class TestNetworkAddrToBinaryString(TestCase):
    def test_ip_address(self):
        binary_addr = network_addr_to_binary_string("192.168.178.41")
        self.assertEqual(binary_addr, "11000000101010001011001000101001")

    def test_invalid_address(self):
        with self.assertRaises(ValueError):
            network_addr_to_binary_string("Not a valid address")


class TestGetSubnetSize(TestCase):
    def test_subnet_size(self):
        subnet_size = get_subnet_size("255.255.255.0")
        self.assertEqual(subnet_size, 24)

    def test_invalid_address(self):
        with self.assertRaisesRegex(ValueError, "Not a valid subnet mask"):
            get_subnet_size("192.168.178.000")


class TestValidSubnetMask(TestCase):
    def test_valid_subnet_mask(self):
        self.assertTrue(valid_subnet_mask("255.255.255.0"))

    def test_invalid_subnet_mask(self):
        self.assertFalse(valid_subnet_mask("Not a valid subnet mask"))
