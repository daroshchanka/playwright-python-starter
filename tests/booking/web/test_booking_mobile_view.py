import pytest
from playwright.sync_api import Page

from project.booking.web.pages.landing_page import LandingPage


@pytest.mark.browser_context_args(
    is_mobile=True,
    viewport={'width': 390, 'height': 830},
    device_scale_factor=2,
)
def test_can_open_close_mobile_menu_drawer(page: Page):
    landing_page = LandingPage(page)
    landing_page.navigate()
    assert landing_page.is_mobile_view_loaded()

    landing_page.open_mobile_menu()
    assert landing_page.is_mobile_menu_opened()
    assert landing_page.is_mobile_menu_careers_item_visible()

    landing_page.close_mobile_menu()
    assert not landing_page.is_mobile_menu_opened()
