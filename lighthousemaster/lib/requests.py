requests = {}


def add_request_from_environ(sid, environ):
    request = environ['aiohttp.request']
    requests[sid] = request
    return request


def remove_request_for_sid(sid):
    requests.pop(sid, None)


def get_request_for_sid(sid):
    return requests.get(sid)
