from marshmallow import Schema, fields
from marshmallow.validate import OneOf


class OAuthAccessTokenSchema(Schema):
    access_token = fields.Str(dump_only=True)
    expires_in = fields.Integer(dump_only=True)
    token_type = fields.Str(dump_only=True)
    grant_type = fields.Str(
        required=True,
        validate=OneOf(
            ('client_credentials',),
            error="grant_type must be set to one of the following: {choices}")
    )
