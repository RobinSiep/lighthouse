from marshmallow import Schema, fields, validates_schema, ValidationError

from lighthouse.lib.crypto import hash_str
from lighthouse.lib.settings import settings


class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valid_creds = settings['user']

    @validates_schema
    def check_credentials(self, data, **kwargs):
        if (self.check_password(data['password']) and data['username'] ==
                self.valid_creds['username']):
            return

        raise ValidationError("Username and password don't match")

    def check_password(self, password):
        hashed_password, _ = hash_str(
            password,
            self.valid_creds['salt'].encode('utf-8')
        )
        return hashed_password == self.valid_creds['hashed_password']
