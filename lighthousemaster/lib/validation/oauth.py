from marshmallow import Schema, fields
from marshmallow.validate import OneOf, Length


class OAuthAccessTokenSchema(Schema):
    access_token = fields.Str(dump_only=True)
    expires_in = fields.Integer(dump_only=True)
    token_type = fields.Str(dump_only=True)
    grant_type = fields.Str(
        required=True,
        validate=OneOf(
            ('client_credentials',),
            error="grant_type must be set to one of the following: {choices}"
        )
    )


class OAuthClientSchema(Schema):
    id = fields.UUID(dump_only=True)
    client_id = fields.UUID(required=True)
    client_secret = fields.Str(
        required=True,
        validate=Length(
            equal=64,
            error="client_secret must be 64 characters long"
        )
    )
    client_type = fields.Str(
        required=True,
        validate=OneOf(
            ('confidential',),
            error="client_type must be set to one of the following: {choises}"
        )
    )
    name = fields.Str(required=True)
