import configparser

from aiohttp import web
import socketio

from lighthouse.db import init_sqlalchemy
from lighthouse.lib.settings import update_settings

sio = socketio.AsyncServer(cors_allowed_origins="*")
app = web.Application()
sio.attach(app)


def main():
    web.run_app(app, port=7102)


def read_settings():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    config.read('local-settings.ini')
    update_settings(config)


def configure():
    read_settings()
    init_sqlalchemy()


configure()


if __name__ == '__main__':
    main()
