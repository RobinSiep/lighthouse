from aiohttp import web
from aiohttp_security import remember

from lighthouse.app import app

routes = web.RouteTableDef()


@routes.post('/auth/login')
async def login(request):
    response = web.json_response()
    await remember(request, response, 'admin')
    return response


app.add_routes(routes)
