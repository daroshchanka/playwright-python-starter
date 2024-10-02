import logging
import pytest

from project.booking.utils.booking_configs import BookingConfigs

log = logging.getLogger()


@pytest.fixture(scope="session")
def project_configs(playwright_cli_configs) -> BookingConfigs:
    return BookingConfigs(playwright_cli_configs['env'])


@pytest.fixture(scope="session", autouse=True)
def browser_context_args(browser_context_args, project_configs):
    opts = {
        **browser_context_args,
        'base_url': project_configs.web_base_url()
    }
    log.info(f"browser_context_args:{opts}")
    return opts
