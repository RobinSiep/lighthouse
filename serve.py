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
async def chat_message(sid, data):
    print("message ", data)
    await sio.emit('reply', room=sid)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app)
