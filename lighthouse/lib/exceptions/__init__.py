from aiohttp.web import HTTPBadRequest, HTTPConflict, HTTPNotFound


class JsonHTTPBadRequest(HTTPBadRequest):
    def __init__(self, json, *args, **kwargs):
        super().__init__(
            text=str(json),
            content_type='application/json',
            *args,
            **kwargs
        )


class JsonHTTPNotFound(HTTPNotFound):
    def __init__(self, json="404: Not found", *args, **kwargs):
        super().__init__(
            text=str(json),
            content_type='application/json',
            *args,
            **kwargs
        )


class JsonHTTPConflict(HTTPConflict):
    def __init__(self, json="409: Conflict", *args, **kwargs):
        super().__init__(
            text=str(json),
            content_type='application/json',
            *args,
            **kwargs
        )
