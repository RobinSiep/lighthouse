import base64

from lighthousemaster.lib.exceptions.oauth import (
    AuthorizationHeaderNotFound, InvalidAuthorizationMethod)


def extract_client_authorization(request):
    try:
        auth_method, encoded_string = request.headers[
            'Authorization'].split(' ')
    except (KeyError, ValueError):
        raise AuthorizationHeaderNotFound

    if not auth_method == 'Basic':
        raise InvalidAuthorizationMethod('Basic')
    decoded_header = base64.b64decode(encoded_string).decode('utf-8')
    client_id, client_secret = decoded_header.split(':')
    return {
        'client_id': client_id,
        'client_secret': client_secret
    }
