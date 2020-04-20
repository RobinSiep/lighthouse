import base64

from sqlalchemy.orm.exc import NoResultFound

from lighthousemaster.lib.exceptions.oauth import (
    AuthorizationHeaderNotFound, InvalidAuthorizationMethod,
    InvalidAuthorizationHeader)
from lighthousemaster.models.oauth import get_token_by_token


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
