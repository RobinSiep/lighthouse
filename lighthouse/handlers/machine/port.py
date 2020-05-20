from aiohttp.web import json_response

from lighthouse.app import sio
from lighthouse.db import save
from lighthouse.handlers.machine import get_machine
from lighthouse.lib.exceptions import JsonHTTPConflict
from lighthouse.lib.routes import routes
from lighthouse.lib.security.decorators import permission_required
from lighthouse.machine import get_active_machine
from lighthouse.models.port import Port


@routes.get("/machines/{id}/ports")
@permission_required('ports')
async def list_ports(request):
    machine = get_machine(request)

    if get_active_machine(machine.sid) is None:
        raise JsonHTTPConflict("The machine is not online")

    async def ports_callback(ports):
        print(ports)

    await sio.emit('emit_ports', to=machine.sid,
                   callback=lambda ports: update_ports(machine, ports))
    return json_response()


def update_ports(machine, ports):
    machine.ports = [Port(number=port, machine_id=machine.id) for port in
                     ports]
    save(machine)
