from functools import wraps

from lighthousemaster.lib.requests import get_request_for_sid
from lighthousemaster.lib.security import validate_access_token


def auth_required(function):
    @wraps(function)
    def wrapped(sid, *args, **kwargs):
        if not validate_access_token(get_request_for_sid(sid)):
            from lighthousemaster import disconnect
            disconnect(sid)
        else:
            return function(*args, **kwargs)
    return wrapped
