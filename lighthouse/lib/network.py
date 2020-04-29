def network_addr_to_binary_string(addr):
    octets = addr.split('.')
    binary_octets = [format(int(octet), '08b') for octet in octets]
    return ''.join(binary_octets)


def get_subnet_size(subnet_mask):
    """ Gets the subnet size from a subnet mask

    With the subnet size we mean the amount of bits of an IP address in the
    subnet that denote the routing prefix.
    """
    return len(network_addr_to_binary_string(subnet_mask).replace('0', ''))
