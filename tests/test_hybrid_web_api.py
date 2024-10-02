import logging
import pytest

from project.booking.utils.booking_configs import BookingConfigs
from project.booking.web.pages.landing_page import LandingPage
from project.httpbin.api.services.anything_service import AnythingService
from project.httpbin.utils.httpbin_configs import HttpbinConfigs

log = logging.getLogger()


@pytest.fixture(scope="session")
def api_context_args(api_context_args, request) -> dict[str, any]:
    project_configs = HttpbinConfigs(request.config.getoption('--ENV'))
    opts = {
        **api_context_args,
        'base_url': project_configs.api_base_url()
    }
    log.info(f"api_context_args:{opts}")
    return opts


@pytest.fixture(scope="session", autouse=True)
def browser_context_args(browser_context_args, request):
    project_configs = BookingConfigs(request.config.getoption('--ENV'))
    opts = {
        **browser_context_args,
        'base_url': project_configs.web_base_url()
    }
    log.info(f"browser_context_args:{opts}")
    return opts


def test_use_web_and_api_context_in_single_test_1(api_request, page):
    landing_page = LandingPage(page)
    landing_page.navigate()
    assert landing_page.is_loaded()

    api_service = AnythingService(api_request)
    query = {'ids': '1,2,3', 'enabled': True}
    response = api_service.get_anything(query)
    assert response.status() == 200


def test_use_web_and_api_context_in_single_test_2(api_request, page):
    landing_page = LandingPage(page)
    landing_page.navigate()
    assert landing_page.is_loaded()

    api_service = AnythingService(api_request)
    query = {'ids': '1,2,3', 'enabled': True}
    response = api_service.get_anything(query)
    assert response.status() == 200
