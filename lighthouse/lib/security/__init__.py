import base64

from aiohttp_security import SessionIdentityPolicy
from aiohttp_security.abc import AbstractAuthorizationPolicy
from sqlalchemy.orm.exc import NoResultFound

from lighthouse.lib.exceptions.oauth import (
    AuthorizationHeaderNotFound, InvalidAuthorizationMethod,
    InvalidAuthorizationHeader)
from lighthouse.models.oauth import get_token_by_token


class LighthouseIdentityPolicy(SessionIdentityPolicy):
    async def identify(self, request):
        if validate_access_token(request):
            return 'oauth'

        return await super().identify(request)


class DefaultAuthorizationPolicy(AbstractAuthorizationPolicy):
    user_permissions = ('connect', 'disconnect', 'wake_on_lan', 'shutdown',
                        'reboot')
    oauth_permissions = ('connect', 'disconnect', 'identify', 'sys_info')

    def __init__(self, user_identity, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_identity = user_identity

    async def authorized_userid(self, identity):
        if identity in ('oauth', self.user_identity):
            return identity

    async def permits(self, identity, permission, context=None):
        permissions = ()
        if identity == self.user_identity:
            permissions = self.user_permissions
        elif identity == 'oauth':
            permissions = self.oauth_permissions

        return permission in permissions


def extract_client_authorization(request):
    try:
        auth_method, encoded_string = request.headers[
            'Authorization'].split(' ')
    except (KeyError, ValueError):
        raise AuthorizationHeaderNotFound

    if not auth_method == 'Basic':
        raise InvalidAuthorizationMethod('Basic')
    decoded_header = base64.b64decode(encoded_string).decode('utf-8')
    try:
        client_id, client_secret = decoded_header.split(':')
    except ValueError:
        raise InvalidAuthorizationHeader(
            "<Method> base64(<client_id>:<client_secret>)"
        )
    return {
        'client_id': client_id,
        'client_secret': client_secret
    }


def validate_access_token(request):
    try:
        auth_method, token_str = request.headers['Authorization'].split(' ')
    except (KeyError, ValueError):
        return False

    if auth_method != 'Bearer':
        return False

    try:
        access_token = get_token_by_token(token_str)
    except NoResultFound:
        return False

    if access_token.client.active and not access_token.expired:
        return True

    return False
