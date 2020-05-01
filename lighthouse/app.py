import argparse
import configparser

import socketio
from aiohttp import web
from aiohttp_security import setup as setup_security
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from lighthouse.db import init_sqlalchemy
from lighthouse.lib.security import (
    DefaultAuthorizationPolicy, LighthouseIdentityPolicy)
from lighthouse.lib.settings import settings, update_settings

sio = socketio.AsyncServer(cors_allowed_origins="*")
app = None

parser = argparse.ArgumentParser()
parser.add_argument(
    '--config', type=str, default="local-settings.ini",
    help="Path to config location. Default is local-settings.ini in "
    "the current directory."
)


def read_settings():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    config.read(get_config_location())
    update_settings(config)


def get_config_location():
    if __name__ == '__main__':
        args = parser.parse_args()
        return args.config
    return 'local-settings.ini'


def configure():
    read_settings()
    init_sqlalchemy()


def init_app():
    global app

    configure()

    middleware = session_middleware(
        EncryptedCookieStorage(
            settings['session']['encryption_key'],
            httponly=False
        )
    )
    app = web.Application(middlewares=[middleware])
    sio.attach(app)


def init_security():
    policy = LighthouseIdentityPolicy()
    setup_security(app, policy, DefaultAuthorizationPolicy())


def main():
    web.run_app(app, port=7102)


init_app()
init_security()

if __name__ == '__main__':
    main()
