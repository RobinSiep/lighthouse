import json

import socketio
from aiohttp import web

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

devices = {}


async def index(request):
    return web.Response(text="Lighthouse", content_type='application/json')


async def list_devices(request):
    return web.json_response(devices)


@sio.event
def connect(sid, environ):
    print("connect ", sid)


@sio.event
async def identify(sid, data):
    print(f"Client identified: {data}")
    devices[sid] = data
    # Temporarily call get_sys_info sync
    await get_sys_info(sid)


async def get_sys_info(sid):
    await sio.emit('sys_info', to=sid)


@sio.event
async def sys_info(sid, sys_info):
    devices[sid].update(sys_info)
    print(json.dumps(devices[sid], indent=4))


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


app.router.add_get('/', index)
app.router.add_get('/devices', list_devices)

if __name__ == '__main__':
    web.run_app(app)
