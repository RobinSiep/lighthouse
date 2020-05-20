from aiohttp_session import get_session

from lighthouse.app import sio
from lighthouse.handlers.auth import *  # noqa
from lighthouse.handlers.machine import *  # noqa
from lighthouse.handlers.machine.port import *  # noqa
from lighthouse.handlers.oauth import *  # noqa
from lighthouse.lib.requests import (add_request_from_environ,
                                     remove_request_for_sid)
from lighthouse.lib.security.decorators import permission_required
from lighthouse.machine import (set_machine, update_machine,
                                set_machine_offline, emit_machines)


@sio.event
async def connect(sid, environ):
    request = add_request_from_environ(sid, environ)
    await connect_client(sid, environ, request)


@permission_required('connect')
async def connect_client(sid, environ, request):
    client_type = 'web'
    session = await get_session(request)
    session['sid'] = sid

    if environ.get('HTTP_USER_AGENT') == "Lighthouse Client":
        client_type = 'machine'
    else:
        await emit_machines()
    print(f"connect {client_type} {sid}")


@sio.event
@permission_required('identify')
async def identify(sid, data):
    print(f"Client identified: {data}")
    await set_machine(sid, data)
    await get_sys_info(sid)


async def get_sys_info(sid):
    await sio.emit('sys_info', to=sid)


@sio.event
@permission_required('sys_info')
async def sys_info(sid, sys_info):
    await update_machine(sid, sys_info)


@sio.event
@permission_required('disconnect')
async def disconnect(sid):
    await set_machine_offline(sid)
    remove_request_for_sid(sid)
    print('disconnect ', sid)
