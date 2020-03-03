import datetime

from aiohttp import web
from aiohttp.web import HTTPBadRequest
from marshmallow import ValidationError

from lighthousemaster.app import app
from lighthousemaster.lib.encrypt import get_secure_token
from lighthousemaster.lib.validation.oauth import OAuthAccessTokenSchema
from lighthousemaster.models.oauth import OAuthAccessToken, get_client

routes = web.RouteTableDef()


@routes.post('/oauth/token')
def create_access_token(request):
    schema = OAuthAccessTokenSchema(strict=True)
    try:
        result = schema.load()
        grant_type = result['grant_type']
    except ValidationError as e:
        raise HTTPBadRequest(
            text=str(e),
            content_type='application/json'
        )

    client = get_client("", "")

    if (grant_type == 'client_credentials' and
            client.client_type != 'confidential'):
        raise HTTPBadRequest(
            text=str({
                'invalid_client': ("Client not authorized to use this "
                                   "grant type")
            }),
            content_type='application/json'
        )

    token = OAuthAccessToken(
        access_token=get_secure_token(),
        client=client,
        expiry_date=(datetime.datetime.now(datetime.timezone.utc) +
                     datetime.timedelta(hours=1)),
        token_type='bearer'
    )

    # TODO persist

    response = web.json_response(schema.dump(token).data)

    #  Response headers according to RFC 6749
    response.headers = {
        'cache_control': 'no-store',
        'pragma': 'no-cache'
    }

    return response


app.add_routes(routes)
