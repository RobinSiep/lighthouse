from aiohttp import web
from aiohttp_security import forget, remember
from marshmallow import ValidationError

from lighthouse.app import app
from lighthouse.lib.exceptions import JsonHTTPBadRequest
from lighthouse.lib.validation.auth import LoginSchema

routes = web.RouteTableDef()


@routes.post('/auth/login')
async def login(request):
    try:
        result = LoginSchema().load(await request.json())
    except ValidationError as e:
        raise JsonHTTPBadRequest(json=str(e))

    response = web.json_response()
    await remember(request, response, result['username'])
    return response


@routes.post('/auth/logout')
async def logout(request):
    response = web.json_response()
    await forget(request, response)
    return response


app.add_routes(routes)
