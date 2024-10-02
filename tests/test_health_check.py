import pytest, logging
from playwright.sync_api import Page, APIRequestContext, Playwright
from typing import Generator

from core.api.http_client import HttpClient

log = logging.getLogger()

@pytest.fixture(scope="session")
def api_request(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    request_context = playwright.request.new_context()
    yield request_context
    request_context.dispose()

def test_playwright_api_context_ok(api_request: APIRequestContext):
    response = api_request.get('https://httpbin.org/get')
    assert response.status == 200
    assert 'Playwright' in response.json()['headers']['User-Agent']
    log.debug('debug log API')

def test_playwright_api_context_ok_2(api_request: APIRequestContext):
    http_client = HttpClient(api_request)
    response = http_client.get('https://httpbin.org/get')
    assert response.status() == 200
    assert 'Playwright' in response.json()['headers']['User-Agent']
    log.debug('debug log API')

def test_playwright_web_context_ok(page: Page):
    page.goto('https://todomvc.com/examples/react/dist/')
    assert 'https://todomvc.com/examples/react/dist/' in page.url
    log.info('info log WEB')


