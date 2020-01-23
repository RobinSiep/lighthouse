import configparser

from aiohttp import web

from lighthousemaster.app import app, sio
from lighthousemaster.db import init_sqlalchemy
from lighthousemaster.lib.settings import update_settings
from lighthousemaster.machine import (set_machine, update_machine,
                                      delete_machine, emit_machines)


def main():
    read_settings()
    init_sqlalchemy()
    web.run_app(app, port=7102)


def read_settings():
    config = configparser.ConfigParser()
    config.read('lighthouse-master/settings.ini')
    config.read('lighthouse-master/local-settings.ini')
    update_settings(config)


@sio.event
async def connect(sid, environ):
    client_type = 'web'
    if environ.get('HTTP_USER_AGENT') == "Lighthouse Client":
        client_type = 'machine'
    else:
        await emit_machines()
    print(f"connect {client_type} {sid}")


@sio.event
async def identify(sid, data):
    print(f"Client identified: {data}")
    await set_machine(sid, data)
    await get_sys_info(sid)


async def get_sys_info(sid):
    await sio.emit('sys_info', to=sid)


@sio.event
async def sys_info(sid, sys_info):
    await update_machine(sid, sys_info)


@sio.event
async def disconnect(sid):
    await delete_machine(sid)
    print('disconnect ', sid)


if __name__ == '__main__':
    main()
