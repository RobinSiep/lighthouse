from aiohttp import web
from aiohttp_security import forget, remember

from lighthouse.lib.decorators import validate_request
from lighthouse.lib.validation.auth import LoginSchema
from lighthouse.lib.routes import routes


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
