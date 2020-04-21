from functools import wraps

from lighthouse.lib.requests import get_request_for_sid
from lighthouse.lib.security import validate_access_token


def auth_required(function):
    @wraps(function)
    async def wrapped(sid, *args, **kwargs):
        request = get_request_for_sid(sid)
        if not request or not validate_access_token(request):
            from lighthouse import disconnect
            return await disconnect(sid)
        else:
            return await function(sid, *args, **kwargs)
    return wrapped
