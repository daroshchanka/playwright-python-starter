import logging
from typing import Self

from playwright.sync_api import Page

log = logging.getLogger()


class BaseWebPage:
    page: Page

    def __init__(self, page: Page):
        self.page = page

    def wait_for_network_idle(self, timeout_sec: int = 10):
        log.debug(f"[Page] wait for state 'networkidle' timeoutSec: {timeout_sec}")
        self.page.wait_for_load_state('networkidle', timeout=timeout_sec * 1000)

    def wait_for_document_loaded(self, timeout_sec: int = 10):
        log.debug(f"[Page] wait for state 'domcontentloaded' timeoutSec: {timeout_sec}")
        self.page.wait_for_load_state('domcontentloaded', timeout=timeout_sec * 1000)

    def pause(self, ms: float):
        self.page.wait_for_timeout(ms)

    def go_to(self, url: str) -> Self:
        self.page.goto(url)
        return self

    def get_url(self) -> str:
        return self.page.url
