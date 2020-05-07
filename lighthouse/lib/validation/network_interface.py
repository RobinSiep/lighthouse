import re

from marshmallow import (EXCLUDE, fields, Schema, validate, validates,
                         post_load, ValidationError)

from lighthouse.lib.network import NETMASK_PATTERN
from lighthouse.models.network_interface import NetworkInterface

IP_ADDRESS_PATTERN = "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"  # noqa


class NetworkInterfaceSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    name = fields.String(required=True,
                         validate=validate.Length(min=1, max=64))
    ip_address = fields.String(data_key='addr', required=True)
    netmask = fields.String(required=True)

    @validates('ip_address')
    def validate_ip_address(self, ip_address):
        if re.match(IP_ADDRESS_PATTERN, ip_address):
            return

        raise ValidationError("Invalid IP address")

    @validates('netmask')
    def validate_netmask(self, netmask):
        if re.match(NETMASK_PATTERN, netmask):
            return

        raise ValidationError("Invalid netmask")

    @post_load
    def parse_to_object(self, data, **kwargs):
        return NetworkInterface(**data)
