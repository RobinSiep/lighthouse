import re

from marshmallow import (EXCLUDE, fields, pre_load, Schema, validate,
                         validates, validates_schema, ValidationError)
from sqlalchemy.orm.exc import NoResultFound

from lighthouse.lib.validation.network_interface import NetworkInterfaceSchema
from lighthouse.lib.validation.port import PortSchema
from lighthouse.models.machine import get_machine_by_name

MAC_ADDRESS_PATTERN = '[0-9A-F]{2}([-:]?)[0-9A-F]{2}(\\1[0-9A-F]{2}){4}$'


class MachineSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.String(dump_only=True)
    sid = fields.String(required=True,
                        validate=validate.Length(equal=32))
    external_ip = fields.String(required=True)
    name = fields.String(required=True,
                         validate=validate.Length(min=1, max=64))
    mac_address = fields.String(required=True,
                                validate=validate.Length(min=1, max=17))

    network_interfaces = fields.List(
        fields.Nested(NetworkInterfaceSchema)
    )
    ports = fields.List(
        fields.Nested(PortSchema)
    )

    @pre_load
    def convert_mac_address_to_uppercase(self, data, **kwargs):
        try:
            data['mac_address'] = data['mac_address'].upper()
        except KeyError:
            # Handled during validation
            pass

        return data

    @validates_schema
    def validate_name(self, data, **kwargs):
        try:
            machine_with_same_name = get_machine_by_name(data['name'])
            if machine_with_same_name.mac_address == data['mac_address']:
                # Same machine
                return

            raise ValidationError(
                "A different machine with this name already exists"
            )
        except NoResultFound:
            return
        except KeyError:
            # Required validation is handled in the schema field declaration
            return

    @validates('mac_address')
    def validate_mac_address_format(self, mac_address):
        if re.match(MAC_ADDRESS_PATTERN, mac_address):
            return

        raise ValidationError("Invalid MAC address format.")
