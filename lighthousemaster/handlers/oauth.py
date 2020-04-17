import datetime

from aiohttp import web
from marshmallow import ValidationError

from lighthousemaster.app import app
from lighthousemaster.db import save
from lighthousemaster.lib.crypto import get_random_token
from lighthousemaster.lib.exceptions import JsonHTTPBadRequest
from lighthousemaster.lib.exceptions.oauth import (
    AuthorizationHeaderNotFound, InvalidAuthorizationMethod)
from lighthousemaster.lib.security import extract_client_authorization
from lighthousemaster.lib.validation.oauth import (
    OAuthAccessTokenSchema, OAuthClientSchema)
from lighthousemaster.models.oauth import OAuthAccessToken, get_client

routes = web.RouteTableDef()


@routes.post('/oauth/token')
async def create_access_token(request):
    schema = OAuthAccessTokenSchema()
    try:
        result = schema.load(await request.json())
        grant_type = result['grant_type']
    except ValidationError as e:
        raise JsonHTTPBadRequest(json=str(e))

    client = get_client_from_request(request)

    if (grant_type == 'client_credentials' and
            client.client_type != 'confidential'):
        raise JsonHTTPBadRequest(json={
            'invalid_client': ("Client not authorized to use this "
                               "grant type")
        })

    token = OAuthAccessToken(
        access_token=get_random_token(32),
        client=client,
        expiry_date=(datetime.datetime.now(datetime.timezone.utc) +
                     datetime.timedelta(hours=1)),
        token_type='Bearer'
    )

    persisted_token, _ = save(token)

    #  Response headers according to RFC 6749
    response = web.json_response(
        schema.dump(persisted_token),
        headers={
            'cache_control': 'no-store',
            'pragma': 'no-cache'
        }
    )

    return response


def get_client_from_request(request):
    try:
        client_credentials = extract_client_authorization(request)
        result = OAuthClientSchema(
            only=('client_id', 'client_secret')
        ).load(client_credentials)
    except (ValidationError, AuthorizationHeaderNotFound,
            InvalidAuthorizationMethod) as e:
        raise JsonHTTPBadRequest(json=str(e))

    return get_client(**result)


app.add_routes(routes)
