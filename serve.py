import json

import socketio
from aiohttp import web

sio = socketio.AsyncServer(cors_allowed_origins="*")
app = web.Application()
sio.attach(app)

machines = {}


async def index(request):
    return web.Response(text="Lighthouse", content_type='application/json')


@sio.event
async def connect(sid, environ):
    client_type = 'web'
    if environ.get('HTTP_USER_AGENT') == "Lighthouse Client":
        client_type = 'machine'
    else:
        await sio.emit('machines', machines)
    print(f"connect {client_type} {sid}")


@sio.event
async def identify(sid, data):
    print(f"Client identified: {data}")
    machines[sid] = data
    await get_sys_info(sid)


async def get_sys_info(sid):
    await sio.emit('sys_info', to=sid)


@sio.event
async def sys_info(sid, sys_info):
    await update_machine(sid, sys_info)
    print(json.dumps(machines[sid], indent=4))


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


@sio.event
async def disconnect(sid):
    await delete_machine(sid)
    print('disconnect ', sid)


app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app)
