import json

import socketio
from aiohttp import web

sio = socketio.AsyncServer(cors_allowed_origins="*")
app = web.Application()
sio.attach(app)

machines = {}


async def index(request):
    return web.Response(text="Lighthouse", content_type='application/json')


async def list_machines(request):
    return web.json_response(machines)


@sio.event
def connect(sid, environ):
    print("connect ", sid)


@sio.event
async def identify(sid, data):
    print(f"Client identified: {data}")
    machines[sid] = data
    # Temporarily call get_sys_info sync
    await get_sys_info(sid)


async def get_sys_info(sid):
    await sio.emit('sys_info', to=sid)


@sio.event
async def sys_info(sid, sys_info):
    print(json.dumps(machines[sid], indent=4))
    update_machine(sid, sys_info)


def update_machine(sid, sys_info):
    machines[sid].update(sys_info)
    await sio.emit('machines', machines)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


app.router.add_get('/', index)
app.router.add_get('/machines', list_machines)

if __name__ == '__main__':
    web.run_app(app)
