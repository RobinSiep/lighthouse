from marshmallow import (Schema, fields, validates_schema, ValidationError,
                         pre_load)

from lighthouse.lib.crypto import hash_str
from lighthouse.lib.settings import settings


class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

    @pre_load
    def read_valid_creds(self, data, **kwargs):
        self.valid_creds = settings['user']
        return data

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
