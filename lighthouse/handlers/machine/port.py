from aiohttp.web import json_response

from lighthouse.app import sio
from lighthouse.handlers.machine import get_machine
from lighthouse.lib.exceptions import JsonHTTPConflict
from lighthouse.lib.routes import routes
from lighthouse.lib.security.decorators import permission_required
from lighthouse.machine import get_active_machine


@routes.get("/machines/{id}/ports")
@permission_required('ports')
async def list_ports(request):
    machine = get_machine(request)

    if get_active_machine(machine.sid) is None:
        raise JsonHTTPConflict("The machine is not online")

    async def ports_callback(ports):
        print(ports)

    await sio.emit('emit_ports', to=machine.sid, callback=ports_callback)
    return json_response()
