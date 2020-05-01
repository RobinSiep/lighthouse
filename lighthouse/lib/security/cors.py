from aiohttp_cors import ResourceOptions, setup as setup_cors

from lighthouse.lib.decorators import singleton


@singleton
class CORS:
    def __init__(self, app):
        self.app = app
        self.cors = setup_cors(app, defaults={
            "*": ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        })

    def sync_routes(self):
        self.add_routes(list(self.app.router.routes()))

    def add_routes(self, routes):
        for route in routes:
            try:
                self.cors.add(route)
            except ValueError:
                pass
