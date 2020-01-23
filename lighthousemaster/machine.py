import uuid

from lighthousemaster.app import sio
from lighthousemaster.db import save
from lighthousemaster.models.machine import Machine, list_machines


async def set_machine(sid, machine_data):
    save(Machine(
        id=str(uuid.uuid4()),
        name=machine_data['name'],
        mac_address='test'
    ))


async def update_machine(sid, sys_info):
    # machines[sid].update(sys_info)
    await sio.emit('machines', list_machines())


async def delete_machine(sid):
    try:
        # machines.pop(sid)
        await sio.emit('machines', list_machines())
    except KeyError:
        # Machine not found for sid, no state update
        pass


async def emit_machines():
    await sio.emit('machines', list_machines())
