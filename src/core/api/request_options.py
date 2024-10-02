import typing

class FilePayload:
    name: str
    mimeType: str
    buffer: bytes

class RequestOptions:
    method: typing.Optional[str] = None
    data: typing.Optional[typing.Union[typing.Any, str, bytes]] = None
    fail_on_status_code: typing.Optional[bool] = None
    form: typing.Optional[typing.Dict[str, typing.Union[str, float, bool]]] = None
    headers: typing.Optional[typing.Dict[str, str]] = None
    ignore_https_errors: typing.Optional[bool] = None
    max_redirects: typing.Optional[int] = None
    max_retries: typing.Optional[int] = None
    multipart: typing.Optional[
        typing.Dict[str, typing.Union[bytes, bool, float, str, FilePayload]]
    ] = None
    params: typing.Optional[
        typing.Union[typing.Dict[str, typing.Union[str, float, bool]], str]
    ] = None
    timeout: typing.Optional[float] = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def set_method(self, method:str):
        self.method = method

    def __repr__(self):
        return ', '.join("%s: %s" % item for item in vars(self).items())
