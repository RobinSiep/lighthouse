from functools import wraps

from marshmallow import ValidationError

from lighthouse.lib.exceptions import JsonHTTPBadRequest


def validate_request(validation_schema):
    def decorate(func):
        @wraps(func)
        async def wrapped(request):
            try:
                result = validation_schema.load(await request.json())
            except ValidationError as e:
                raise JsonHTTPBadRequest(json=str(e))
            return await func(request, result)
        return wrapped
    return decorate
