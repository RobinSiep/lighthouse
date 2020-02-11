from marshmallow import fields, Schema, validate


class MachineSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True,
                         validate=validate.Length(min=1, max=64))
    mac_address = fields.String(required=True,
                                validate=validate.Length(mix=1, max=17))
