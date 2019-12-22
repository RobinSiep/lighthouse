from lighthousemaster.app import sio

machines = {}


async def set_machine(sid, machine_data):
    machines[sid] = machine_data


async def update_machine(sid, sys_info):
    machines[sid].update(sys_info)
    await sio.emit('machines', machines)


async def delete_machine(sid):
    try:
        machines.pop(sid)
        await sio.emit('machines', machines)
    except KeyError:
        # Machine not found for sid, no state update
        pass


async def emit_machines():
    await sio.emit('machines', machines)
