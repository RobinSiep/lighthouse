from aiohttp.web import HTTPBadRequest


class JsonHTTPBadRequest(HTTPBadRequest):
    def __init__(self, json, *args, **kwargs):
        super().__init__(
            text=str(json),
            content_type='application/json',
            *args,
            **kwargs
        )
