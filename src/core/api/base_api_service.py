from playwright.sync_api import APIRequestContext

from core.api.http_client import HttpClient

class BaseApiService:
    base_url: str
    http_client: HttpClient

    def __init__(self, context: APIRequestContext, base_url: str = ''):
        self.http_client = HttpClient(context)
        self.base_url = base_url