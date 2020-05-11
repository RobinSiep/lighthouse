from aiohttp import web

from lighthouse.app import sio
from lighthouse.lib.routes import routes
from lighthouse.lib.security.decorators import permission_required
from lighthouse.machine import get_active_machine_on_same_subnet
from lighthouse.models.machine import get_machine_by_id


@routes.post("/machines/{id}/wake")
@permission_required('wake_on_lan')
async def send_wake_on_LAN_packet(request):
    machine = get_machine_by_id(request.match_info['id'])
    if not machine:
        return web.json_response(status=404)

    capable_machine = get_active_machine_on_same_subnet(machine)
    if not capable_machine:
        return web.json_response(
            "No machine was found capable of waking up the requested machine",
            status=409
        )

    await sio.emit(
        'send_wake_on_LAN_packet',
        machine.mac_address,
        to=capable_machine.sid
    )
    return web.json_response()


@routes.post("/machines/{id}/shutdown")
@permission_required('shutdown')
async def shutdown(request):
    machine = get_machine_by_id(request.match_info['id'])
    if not machine:
        return web.json_response(status=404)

    await sio.emit('shutdown', to=machine.sid, callback=shutdown_callback)
    return web.json_response()


def shutdown_callback(status, error=None):
    print(status)
    print(error)
