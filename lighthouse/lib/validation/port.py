from marshmallow import EXCLUDE, fields, Schema


class PortSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    number = fields.Integer(required=True)
    forwarded = fields.Bool(required=True)
