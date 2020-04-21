import uuid

from sqlalchemy.orm.exc import NoResultFound

from lighthouse.app import sio
from lighthouse.db import save
from lighthouse.lib.validation.machine import MachineSchema
from lighthouse.models.machine import (Machine, list_machines,
                                             get_machine_by_mac_address)

machine_sys_info = {}


async def set_machine(sid, machine_data):
    machine_data['sid'] = sid
    validated_data = MachineSchema().load(machine_data)

    try:
        machine = get_machine_by_mac_address(validated_data['mac_address'])
        machine.set_fields(validated_data)
    except NoResultFound:
        machine = Machine(
            id=str(uuid.uuid4()),
            **validated_data
        )

    machine_sys_info[sid] = {}
    save(machine)


async def update_machine(sid, sys_info):
    machine_sys_info[sid] = sys_info
    await sio.emit('machines', dump_machines())


async def set_machine_offline(sid):
    try:
        machine_sys_info.pop(sid)
        await sio.emit('machines', dump_machines())
    except KeyError:
        # Machine not found for sid, no state update
        pass


async def emit_machines():
    await sio.emit('machines', dump_machines())


def dump_machines():
    return list(map(merge_machine_and_sys_info, list_machines()))


def merge_machine_and_sys_info(machine):
    machine_data = MachineSchema().dump(machine)
    try:
        machine_data['sys_info'] = machine_sys_info[machine.sid]
    except KeyError:
        pass

    return machine_data