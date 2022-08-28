import requests

from functools import wraps

from zakka.conf import settings, user_agent


class DjangoSession(requests.Session):
    def __init__(self, distribution_name=settings.USER_AGENT_DISTRIBUTION):
        super().__init__()
        self.headers["user-agent"] = user_agent(distribution_name)


@wraps(requests.request, assigned=["__doc__"])
def request(method, url, **kwargs):
    with DjangoSession() as session:
        return session.request(method=method, url=url, **kwargs)


@wraps(requests.get, assigned=["__doc__"])
def get(url, **kwargs) -> requests.Response:
    return request("get", url, **kwargs)


@wraps(requests.head, assigned=["__doc__"])
def head(url, **kwargs) -> requests.Response:
    return request("head", url, **kwargs)


@wraps(requests.options, assigned=["__doc__"])
def options(url, **kwargs) -> requests.Response:
    return request("options", url, **kwargs)


@wraps(requests.post, assigned=["__doc__"])
def post(url, data=None, json=None, **kwargs) -> requests.Response:
    return request("post", url, data=data, json=json, **kwargs)


@wraps(requests.put, assigned=["__doc__"])
def put(url, data=None, **kwargs) -> requests.Response:
    return request("put", url, data=data, **kwargs)


@wraps(requests.patch, assigned=["__doc__"])
def patch(url, data=None, **kwargs) -> requests.Response:
    return request("patch", url, data=data, **kwargs)


@wraps(requests.delete, assigned=["__doc__"])
def delete(url, **kwargs) -> requests.Response:
    return request("delete", url, **kwargs)
