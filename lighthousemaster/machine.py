import uuid

from sqlalchemy.orm.exc import NoResultFound

from lighthousemaster.app import sio
from lighthousemaster.db import save
from lighthousemaster.lib.validation.machine import MachineSchema
from lighthousemaster.models.machine import (Machine, list_machines,
                                             get_machine_by_name)

machine_sys_info = {}


async def set_machine(sid, machine_data):
    print(sid)
    validated_data = MachineSchema().load(machine_data)

    try:
        machine = get_machine_by_name(validated_data['name'])
        machine.set_fields(validated_data)
    except NoResultFound:
        machine = Machine(
            id=str(uuid.uuid4()),
            **validated_data
        )

    machine_sys_info[sid] = {}
    save(machine)


async def update_machine(sid, sys_info):
    machine_sys_info[sid].update(sys_info)
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
        machine_data['sys_info'] = machine_sys_info(machine.sid)
    except:
        pass

    return machine_data
