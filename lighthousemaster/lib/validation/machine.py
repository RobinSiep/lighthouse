import re

from marshmallow import (EXCLUDE, fields, pre_load, Schema, validate,
                         validates, ValidationError)
from sqlalchemy.orm.exc import NoResultFound

from lighthousemaster.models.machine import get_machine_by_name

MAC_ADDRESS_PATTERN = '[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$'


class MachineSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.String(dump_only=True)
    sid = fields.String(dump_only=True)
    name = fields.String(required=True,
                         validate=validate.Length(min=1, max=64))
    mac_address = fields.String(required=True,
                                validate=validate.Length(min=1, max=17))

    @pre_load
    def convert_mac_address_to_uppercase(self, data, **kwargs):
        try:
            data['mac_address'] = data['mac_address'].upper()
        except KeyError:
            # Handled during validation
            return

    @validates('name')
    def validate_name(self, name):
        try:
            machine_with_same_name = get_machine_by_name(name)
            if machine_with_same_name.sid == self.context['sid']:
                # Same machine
                return

            raise ValidationError(
                "A different machine with this name already exists"
            )
        except NoResultFound:
            return

    @validates('mac_address')
    def validate_mac_address_format(self, mac_address):
        if re.match(MAC_ADDRESS_PATTERN, mac_address):
            return

        raise ValidationError("Invalid MAC address format.")
