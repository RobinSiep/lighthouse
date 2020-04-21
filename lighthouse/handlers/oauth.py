import datetime

from aiohttp import web
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from lighthouse.app import app
from lighthouse.db import save
from lighthouse.lib.crypto import get_random_token
from lighthouse.lib.exceptions import JsonHTTPBadRequest
from lighthouse.lib.exceptions.oauth import (
    AuthorizationHeaderNotFound, InvalidAuthorizationMethod,
    InvalidAuthorizationHeader)
from lighthouse.lib.security import extract_client_authorization
from lighthouse.lib.validation.oauth import (
    OAuthAccessTokenSchema, OAuthClientSchema)
from lighthouse.models.oauth import OAuthAccessToken, get_client

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
            InvalidAuthorizationMethod, InvalidAuthorizationHeader) as e:
        raise JsonHTTPBadRequest(json=str(e))

    try:
        return get_client(**result)
    except NoResultFound:
        raise JsonHTTPBadRequest(json="No client found for given client_id")


app.add_routes(routes)
