from marshmallow import EXCLUDE, fields, Schema, validate, post_load

from lighthouse.models.network_interface import NetworkInterface


class NetworkInterfaceSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    name = fields.String(required=True,
                         validate=validate.Length(min=1, max=64))
    ip_address = fields.String(data_key='addr', required=True)
    netmask = fields.String(required=True)

    @post_load
    def parse_to_object(self, data, **kwargs):
        return NetworkInterface(**data)
