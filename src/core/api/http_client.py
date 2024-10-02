import logging

from playwright.sync_api import APIRequestContext

from core.api.request_options import RequestOptions
from core.api.response import Response


class HttpClient:
    api_request: APIRequestContext
    log = logging.getLogger()

    def __init__(self, context: APIRequestContext):
        self.api_request = context

    def delete(self, url: str, options: RequestOptions = RequestOptions()):
        return self.request('delete', url, options)

    def get(self, url: str, options: RequestOptions = RequestOptions()):
        return self.request('get', url, options)

    def head(self, url: str, options: RequestOptions = RequestOptions()):
        return self.request('head', url, options)

    def post(self, url: str, options: RequestOptions = RequestOptions()):
        return self.request('post', url, options)

    def put(self, url: str, options: RequestOptions = RequestOptions()):
        return self.request('put', url, options)

    def patch(self, url: str, options: RequestOptions = RequestOptions()):
        return self.request('patch', url, options)

    def request(self, method: str, url: str, options: RequestOptions = RequestOptions()):
        self.log.debug(f"{method.upper()} {url} --> \nrequest:{{{repr(options)}}}")
        options.set_method(method)
        playwright_response = self.api_request.fetch(url, **vars(options))
        result = Response(playwright_response)
        self.log.debug(f" < -- {method.upper()} {url} - {result.status()}")
        return result
