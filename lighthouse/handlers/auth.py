from aiohttp import web
from aiohttp_security import forget, remember

from lighthouse.app import app
from lighthouse.lib.decorators import validate_request
from lighthouse.lib.security.cors import sync_routes
from lighthouse.lib.validation.auth import LoginSchema

routes = web.RouteTableDef()


@routes.post('/auth/login')
@validate_request(LoginSchema())
async def login(request, result):
    response = web.json_response()
    await remember(request, response, result['username'])
    return response


@routes.post('/auth/logout')
async def logout(request):
    response = web.json_response()
    await forget(request, response)
    return response


app.add_routes(routes)
sync_routes(app)
