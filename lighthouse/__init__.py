import configparser

from aiohttp import web

from lighthouse.app import app, sio
from lighthouse.db import init_sqlalchemy
from lighthouse.handlers.oauth import *  # noqa
from lighthouse.lib.requests import (add_request_from_environ,
                                           remove_request_for_sid)
from lighthouse.lib.security import validate_access_token
from lighthouse.lib.security.decorators import auth_required
from lighthouse.lib.settings import update_settings
from lighthouse.machine import (set_machine, update_machine,
                                      set_machine_offline, emit_machines)


def main():
    read_settings()
    init_sqlalchemy()
    web.run_app(app, port=7102)


def read_settings():
    config = configparser.ConfigParser()
    config.read('lighthouse/settings.ini')
    config.read('lighthouse/local-settings.ini')
    update_settings(config)


@sio.event
async def connect(sid, environ):
    request = add_request_from_environ(sid, environ)
    client_type = 'web'
    if environ.get('HTTP_USER_AGENT') == "Lighthouse Client":
        if not (validate_access_token(request)):
            return False
        client_type = 'machine'
    else:
        await emit_machines()
    print(f"connect {client_type} {sid}")


@sio.event
@auth_required
async def identify(sid, data):
    print(f"Client identified: {data}")
    await set_machine(sid, data)
    await get_sys_info(sid)


async def get_sys_info(sid):
    await sio.emit('sys_info', to=sid)


@sio.event
@auth_required
async def sys_info(sid, sys_info):
    await update_machine(sid, sys_info)


@sio.event
async def disconnect(sid):
    await set_machine_offline(sid)
    remove_request_for_sid(sid)
    print('disconnect ', sid)


if __name__ == '__main__':
    main()
