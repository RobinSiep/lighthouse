import re

NETMASK_PATTERN = "^(((255\\.){3}(255|254|252|248|240|224|192|128|0+))|((255\\.){2}(255|254|252|248|240|224|192|128|0+)\\.0)|((255\\.)(255|254|252|248|240|224|192|128|0+)(\\.0+){2})|((255|254|252|248|240|224|192|128|0+)(\\.0+){3}))$"  # noqa


def network_addr_to_binary_string(addr):
    octets = addr.split('.')
    try:
        binary_octets = [format(int(octet), '08b') for octet in octets]
    except ValueError:
        raise ValueError("Invalid address given")
    return ''.join(binary_octets)


def get_subnet_size(subnet_mask):
    """ Gets the subnet size from a subnet mask

    With the subnet size we mean the amount of bits of an IP address in the
    subnet that denote the routing prefix.
    """
    if not valid_subnet_mask(subnet_mask):
        raise ValueError("Not a valid subnet mask")

    return len(network_addr_to_binary_string(subnet_mask).replace('0', ''))


def valid_subnet_mask(subnet_mask):
    return re.match(NETMASK_PATTERN, subnet_mask)
