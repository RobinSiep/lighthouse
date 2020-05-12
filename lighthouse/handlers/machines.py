from aiohttp.web import json_response
from aiohttp_session import get_session

from lighthouse.app import sio
from lighthouse.lib.exceptions import JsonHTTPNotFound
from lighthouse.lib.routes import routes
from lighthouse.lib.security.decorators import permission_required
from lighthouse.machine import get_active_machine_on_same_subnet
from lighthouse.models.machine import get_machine_by_id


def get_machine(request):
    machine = get_machine_by_id(request.match_info['id'])
    if not machine:
        raise JsonHTTPNotFound()
    return machine


@routes.post("/machines/{id}/wake")
@permission_required('wake_on_lan')
async def send_wake_on_LAN_packet(request):
    machine = get_machine(request)
    capable_machine = get_active_machine_on_same_subnet(machine)
    if not capable_machine:
        return json_response(
            "No machine was found capable of waking up "
            "the requested machine",
            status=409
        )

    await sio.emit(
        'send_wake_on_LAN_packet',
        machine.mac_address,
        to=capable_machine.sid
    )
    return json_response()


@routes.post("/machines/{id}/shutdown")
@permission_required('shutdown')
async def shutdown(request):
    machine = get_machine(request)
    session = await get_session(request)
    sid = session.get('sid')

    await sio.emit(
        'shutdown',
        to=machine.sid,
        callback=lambda status, error: shutdown_callback(status, error, sid)
    )
    return json_response()


def shutdown_callback(status, error=None, sid=None):
    if not status:
        print(f"Machine shutdown failed: {error}")

    if sid:
        sio.emit('response', status, error, to=sid)
