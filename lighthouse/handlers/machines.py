from aiohttp import web

from lighthouse.app import app, sio
from lighthouse.lib.security.cors import sync_routes
from lighthouse.lib.security.decorators import permission_required
from lighthouse.models.machine import get_machine_by_id

routes = web.RouteTableDef()


@routes.post("/machines/{id}/wake")
@permission_required('wake_on_lan')
async def send_wake_on_LAN_packet(request):
    machine = get_machine_by_id(request.match_info['id'])
    # TODO prototype data
    capable_machine = get_machine_by_id('6daad3f2-dc11-4c6d-bc31-0d66399d2bf3')
    await sio.emit(
        'send_wake_on_LAN_packet',
        machine.mac_address,
        to=capable_machine.sid
    )
    return web.json_response()


app.add_routes(routes)
sync_routes(app)
