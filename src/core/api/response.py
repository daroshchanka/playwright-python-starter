import functools
import logging
import typing

from playwright.sync_api import APIResponse

log = logging.getLogger()


class Response:
    playwright_response: APIResponse

    def __init__(self, playwright_response: APIResponse):
        self.playwright_response = playwright_response

    @functools.cache
    def json(self) -> typing.Any:
        json = self.playwright_response.json()
        log.debug(f'JSON: {json}')
        return json

    def status(self) -> int:
        return self.playwright_response.status

    @functools.cache
    def text(self) -> str:
        return self.playwright_response.text()

    @functools.cache
    def body(self) -> bytes:
        return self.playwright_response.body()

    @functools.cache
    def headers(self) -> typing.Optional[typing.Dict[str, str]]:
        return self.playwright_response.headers

    def get_wrapped(self) -> APIResponse:
        return self.playwright_response
