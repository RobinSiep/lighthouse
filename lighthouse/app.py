import argparse
import configparser

import socketio
from aiohttp import web
from aiohttp_security import setup as setup_security
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from lighthouse.db import init_sqlalchemy
from lighthouse.lib.routes import routes
from lighthouse.lib.security import (
    DefaultAuthorizationPolicy, LighthouseIdentityPolicy)
from lighthouse.lib.security.cors import CORS
from lighthouse.lib.settings import settings, update_settings

sio = socketio.AsyncServer(cors_allowed_origins="*")

parser = argparse.ArgumentParser()
parser.add_argument(
    '--config', type=str, default="local-settings.ini",
    help="Path to config location. Default is local-settings.ini in "
    "the current directory."
)
args = None


def main():
    global args

    args = parser.parse_args()
    app = app_factory()
    web.run_app(app, port=7102)


def app_factory():
    configure()
    return init_app()


def init_app():
    session_settings = settings['session']
    middleware = session_middleware(
        EncryptedCookieStorage(
            session_settings['encryption_key'],
            max_age=int(session_settings['max_age']),
            httponly=False
        )
    )
    app = web.Application(middlewares=[middleware])
    sio.attach(app)

    init_security(app)
    app.add_routes(routes)
    CORS(app).sync_routes()

    return app


def configure():
    read_settings()
    init_sqlalchemy()


def read_settings():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    config.read(get_config_location())
    update_settings(config)


def get_config_location():
    if args:
        return args.config
    return 'local-settings.ini'


def init_security(app):
    policy = LighthouseIdentityPolicy()
    setup_security(
        app,
        policy,
        DefaultAuthorizationPolicy(settings['user']['username'])
    )


if __name__ == '__main__':
    main()
