import configparser

import socketio
from aiohttp import web
from aiohttp_security import SessionIdentityPolicy, setup as setup_security
from aiohttp_session import SimpleCookieStorage, session_middleware

from lighthouse.db import init_sqlalchemy
from lighthouse.lib.security import DefaultAuthorizationPolicy
from lighthouse.lib.settings import update_settings

sio = socketio.AsyncServer(cors_allowed_origins="*")
middleware = session_middleware(SimpleCookieStorage())
app = web.Application(middlewares=[middleware])
sio.attach(app)


def main():
    web.run_app(app, port=7102)


def init_security():
    policy = SessionIdentityPolicy()
    setup_security(app, policy, DefaultAuthorizationPolicy())


def read_settings():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    config.read('local-settings.ini')
    update_settings(config)


def configure():
    read_settings()
    init_sqlalchemy()


configure()
init_security()


if __name__ == '__main__':
    main()
