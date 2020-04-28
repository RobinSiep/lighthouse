from functools import wraps

from aiohttp.web import BaseRequest
from aiohttp_security import check_permission

from lighthouse.lib.requests import get_request_for_sid


def permission_required(permission):
    def decorate(func):
        @wraps(func)
        async def wrapped(sid_or_request, *args, **kwargs):
            if isinstance(sid_or_request, BaseRequest):
                request = sid_or_request
            else:
                request = get_request_for_sid(sid_or_request)

            await check_permission(request, permission)
            return await func(sid_or_request, *args, **kwargs)
        return wrapped
    return decorate
