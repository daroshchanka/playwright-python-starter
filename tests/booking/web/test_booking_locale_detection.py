import pytest
from playwright.sync_api import Page

from core.web.base_web_page import BaseWebPage


@pytest.mark.browser_context_args(locale='fr-FR')
def test_user_should_be_redirected_to_the_target_locate_index_page(page: Page):
    base_page = BaseWebPage(page)
    base_page.go_to('/').wait_for_network_idle(10)
    assert '/index.fr.html' in base_page.get_url()