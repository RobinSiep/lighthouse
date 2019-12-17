import json

import socketio
from aiohttp import web

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


async def index(request):
    """Serve the client-side application."""
    return web.Response(text="Hello world", content_type='application/json')


@sio.event
def connect(sid, environ):
    print("connect ", sid)


@sio.event
async def identify(sid, data):
    print(f"Client identified: {data}")
    # Temporarily call get_sys_info sync
    await get_sys_info(sid)


async def get_sys_info(sid):
    await sio.emit('sys_info', to=sid, callback=recv_sys_info)


def recv_sys_info(sys_info):
    print(json.dumps(sys_info, indent=4))


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app)
