import asyncio

from aiohttp.web import json_response
from aiohttp_session import get_session

from lighthouse.app import sio
from lighthouse.lib.exceptions import JsonHTTPConflict, JsonHTTPNotFound
from lighthouse.lib.routes import routes
from lighthouse.lib.security.decorators import permission_required
from lighthouse.machine import (
    get_active_machine, get_active_machine_on_same_subnet)
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
    await _wake(
        machine,
        get_wake_on_LAN_capable_machine(machine)
    )
    return json_response()


def get_wake_on_LAN_capable_machine(target_machine):
    wol_capable_machine = get_active_machine_on_same_subnet(target_machine)
    if not wol_capable_machine:
        raise JsonHTTPConflict(
            "No machine was found capable of waking up "
            "the requested machine"
        )
    return wol_capable_machine


async def _wake(target_machine, wol_capable_machine):
    await sio.emit(
        'send_wake_on_LAN_packet',
        target_machine.mac_address,
        to=wol_capable_machine.sid
    )


@routes.post("/machines/{id}/shutdown")
@permission_required('shutdown')
async def shutdown(request):
    machine = get_machine(request)
    if get_active_machine(machine.sid) is None:
        raise JsonHTTPConflict("The machine is not online")

    session = await get_session(request)
    sid = session.get('sid')
    await _shutdown(machine, sid)

    return json_response()


async def _shutdown(machine, requesting_sid):
    await sio.emit(
        'shutdown',
        to=machine.sid,
        callback=lambda status, error: shutdown_callback(
            status, error, requesting_sid
        )
    )


@routes.post("/machines/{id}/reboot")
@permission_required('reboot')
async def reboot(request):
    machine = get_machine(request)
    wol_capable_machine = get_wake_on_LAN_capable_machine(machine)

    if get_active_machine(machine.sid) is None:
        await _wake(machine.sid, wol_capable_machine)
        return json_response()

    session = await get_session(request)
    sid = session.get('sid')
    await _shutdown(machine, sid)

    async def disconnect_callback():
        _wake(machine.sid, wol_capable_machine),

    await poll_for_disconnect(machine.sid, disconnect_callback, 5, 60)


async def poll_for_disconnect(sid, callback, interval_in_s, max_time_in_s):
    for i in range(0, max_time_in_s, interval_in_s):
        await asyncio.sleep(interval_in_s)
        if get_active_machine(sid) is None:
            await callback()
            return
    await callback()


async def shutdown_callback(status, error=None, sid=None):
    if not status:
        print(f"Machine shutdown failed: {error}")

    if sid:
        await sio.emit('response', (status, error), to=sid)
