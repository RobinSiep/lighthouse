from aiohttp_cors import ResourceOptions, setup as setup_cors

from lighthouse.app import app

cors = setup_cors(app, defaults={
    "*": ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    )
})


def sync_routes(app):
    add_routes(list(app.router.routes()))


def add_routes(routes):
    for route in routes:
        try:
            cors.add(route)
        except ValueError:
            pass
