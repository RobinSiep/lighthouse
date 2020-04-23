from functools import wraps

from aiohttp_security import check_permission

from lighthouse.lib.requests import get_request_for_sid


def permission_required(permission):
    def decorate(func):
        @wraps(func)
        async def wrapped(sid, *args, **kwargs):
            await check_permission(get_request_for_sid(sid), permission)
            return await func(sid, *args, **kwargs)
        return wrapped
    return decorate
